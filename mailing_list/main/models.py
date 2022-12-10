import pytz
import re

from django.db import models

from .validators import phone_validator


class MailingList(models.Model):
    start = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end = models.DateTimeField(verbose_name='Дата и время конца рассылки')
    text = models.TextField(verbose_name='Текст рассылки')
    tags = models.CharField(verbose_name='Теги поиска', max_length=25)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка {self.pk}'

    @property
    def get_tags(self):
        return re.sub("[^\w]", " ",  self.tags).split()


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.PositiveIntegerField(
        verbose_name='Номер Телефона', validators=[phone_validator])
    code = models.PositiveIntegerField(
        verbose_name='Код оператора')
    tags = models.CharField(verbose_name='Теги поиска', max_length=25)
    timezone = models.CharField(
        verbose_name='Time zone', max_length=32, choices=TIMEZONES, default='UTC')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент {self.pk} с номером {self.phone_number}'

    @property
    def get_tags(self):
        return re.sub("[^\w]", " ",  self.tags).split()


class Message(models.Model):
    SENT = "Sent"
    PROCEEDED = "Proceeded"

    STATUS_CHOICES = [
        (SENT, "Sent"),
        (PROCEEDED, "Proceeded"),
    ]

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    date_time = models.DateTimeField(auto_now_add=True,
        verbose_name='Дата и время сообщения')
    status = models.CharField(verbose_name='Статус',
                              choices=STATUS_CHOICES, max_length=25)
    mail_list = models.ForeignKey(
        MailingList, verbose_name='Рассылка', related_name='messages', on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, verbose_name='Клиент', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f'Сообщение {self.pk} с текстом {self.mail_list.text} для {self.client}'
