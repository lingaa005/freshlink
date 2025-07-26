from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import VendorGroupChatMessage,Producer,Rating
from .serializers import (
    VendorGroupChatMessageSerializer,ProducerSerializer,ProducerDetailSerializer
    ,ProducerReviewSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
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
class VendorProducerListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only check if user is logged in

    def get(self, request):
        user = request.user

        # Inline vendor permission check
        if not hasattr(user, 'vendor'):
            return Response({'detail': 'Only vendors can access this resource.'}, status=status.HTTP_403_FORBIDDEN)

        producers = Producer.objects.all()
        serializer = ProducerSerializer(producers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProducerDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, producer_id):
        user = request.user

        # Only vendors or admins can access
        if user.role not in ['vendor', 'admin']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            producer = Producer.objects.get(id=producer_id)
        except Producer.DoesNotExist:
            return Response({'detail': 'Producer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProducerDetailSerializer(producer)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProducerOwnReviewsAPIView(generics.ListAPIView):
    serializer_class = ProducerReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role != 'producer':
            raise PermissionDenied("Only producers can view their reviews.")

        producer = Producer.objects.get(user=user)
        return Rating.objects.filter(producer=producer).select_related('vendor__user')
