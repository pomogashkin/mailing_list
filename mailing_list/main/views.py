from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import MailingList, Client, Message
from .serializers import MailingListSerializer, MailingInfoSerializer, ClientSerializer, MessageSerializer
from .tasks import send_mails


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^tags',)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('mail_list__tags',)


class MailingListViewSet(viewsets.ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^tags',)

    @action(detail=True, url_path='info')
    def info(self, request, pk=None):
        """
        Данные по конкретной рассылке
        """
        mailing = get_object_or_404(MailingList.objects.all(), pk=pk)
        serializer = MailingInfoSerializer(mailing)
        return Response(serializer.data)

    @action(detail=False, url_path='full-info')
    def fullinfo(self, request):
        """
        Данные по всем рассылкам
        """
        queryset = MailingList.objects.all()
        serializer = MailingInfoSerializer(
            queryset, many=True)
        return Response(serializer.data)
