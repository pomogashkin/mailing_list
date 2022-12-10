from rest_framework import serializers
from .models import MailingList, Client, Message


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingInfoSerializer(serializers.ModelSerializer):
    sent_messages = serializers.SerializerMethodField()
    messages_to_send = serializers.SerializerMethodField()
    clients = serializers.SerializerMethodField()

    class Meta:
        model = MailingList
        fields = ('id', 'start', 'end', 'text', 'tags',
                  'sent_messages', 'messages_to_send',)

    def get_sent_messages(self, obj):
        return len(obj.messages.filter(status='Sent'))

    def get_messages_to_send(self, obj):
        return len(obj.messages.filter(status='Proceeded'))
