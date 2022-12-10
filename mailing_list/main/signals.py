from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MailingList, Client, Message
from .tasks import send_mails


@receiver(post_save, sender=MailingList)
def create_message(sender, instance, created, **kwargs):
    if created:
        print('пошло')
        mailing = MailingList.objects.filter(pk=instance.pk).first()
        mail_tags = mailing.get_tags
        clients = [client
                   for client in Client.objects.all()
                   for client_tag in client.get_tags
                   if client_tag in mail_tags
                   ]

        for client in clients:
            message = Message.objects.create(
                status="Proceeded",
                client_id=client.pk,
                mail_list_id=instance.pk
            )
            data = {
                'id': message.id,
                "phone": client.phone_number,
                "text": mailing.text
            }
            client_id = client.id
            mailing_id = mailing.id
            print(instance.start)
            if instance.start.timestamp() < datetime.now().timestamp() < instance.end.timestamp():
                send_mails.apply_async((data,),
                                       expires=instance.end)
            else:
                send_mails.apply_async((data,),
                                       eta=instance.start, expires=instance.end)
