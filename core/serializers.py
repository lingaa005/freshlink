from rest_framework import serializers
from .models import VendorGroupChatMessage

class VendorGroupChatMessageSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.user.username', read_only=True)

    class Meta:
        model = VendorGroupChatMessage
        fields = ['id', 'vendor', 'vendor_name', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'vendor_name', 'vendor']
