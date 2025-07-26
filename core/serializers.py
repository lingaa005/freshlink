from rest_framework import serializers
from .models import VendorGroupChatMessage,Producer,Vendor,User,Rating
from django.db.models import Avg


class VendorGroupChatMessageSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.user.username', read_only=True)

    class Meta:
        model = VendorGroupChatMessage
        fields = ['id', 'vendor', 'vendor_name', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'vendor_name', 'vendor']
class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'company_name', 'fssai_license', 'contact_info']

class ProducerDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()  # 👈 Add this line

    class Meta:
        model = Producer
        fields = [
            'id', 'company_name', 'fssai_license',
            'contact_info', 'flagged_review_count',
            'reported_to_govt', 'average_rating',
            'total_reviews', 'reviews'  # 👈 Add this
        ]

    def get_average_rating(self, obj):
        avg = Rating.objects.filter(producer=obj).aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg else None

    def get_total_reviews(self, obj):
        return Rating.objects.filter(producer=obj).count()

    def get_reviews(self, obj):
        return list(Rating.objects.filter(producer=obj).values_list('review', flat=True))
class ProducerReviewSerializer(serializers.ModelSerializer):
    vendor = serializers.CharField(source='vendor.user.username')

    class Meta:
        model = Rating
        fields = ['id', 'vendor', 'rating', 'review', 'is_safety_concern', 'created_at']
class RatingCreateSerializer(serializers.ModelSerializer):
    producer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Rating
        fields = ['producer_id', 'rating', 'review', 'is_safety_concern']

    def validate_producer_id(self, value):
        if not Producer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Producer not found.")
        return value

    def create(self, validated_data):
        vendor = self.context['request'].user.vendor
        producer = Producer.objects.get(id=validated_data.pop('producer_id'))

        # Optional: prevent duplicate reviews
        if Rating.objects.filter(vendor=vendor, producer=producer).exists():
            raise serializers.ValidationError("You have already rated this producer.")

        return Rating.objects.create(vendor=vendor, producer=producer, **validated_data)
