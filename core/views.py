from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import VendorGroupChatMessage
from .serializers import VendorGroupChatMessageSerializer
from .models import Vendor  # adjust import path if needed

class VendorGroupChatListCreateAPIView(generics.ListCreateAPIView):
    queryset = VendorGroupChatMessage.objects.all().order_by('timestamp')
    serializer_class = VendorGroupChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'vendor':
            raise PermissionDenied("Only vendors can send group chat messages.")
        try:
            vendor = Vendor.objects.get(user=user)
        except Vendor.DoesNotExist:
            raise PermissionDenied("Vendor profile not found.")
        serializer.save(vendor=vendor)
