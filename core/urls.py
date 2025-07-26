from django.urls import path
from .views import (VendorGroupChatListCreateAPIView,VendorProducerListAPIView,ProducerDetailAPIView
,ProducerOwnReviewsAPIView,SubmitRatingView
)
urlpatterns = [
    path('vendor-chat/', VendorGroupChatListCreateAPIView.as_view(), name='vendor-chat'),
    path('producers/', VendorProducerListAPIView.as_view(), name='vendor-producer-list'),
    path('producers/<int:producer_id>/', ProducerDetailAPIView.as_view(), name='producer-detail'),
    path('producers/reviews/', ProducerOwnReviewsAPIView.as_view(), name='producer-own-reviews'),
    path('rate-producers/', SubmitRatingView.as_view(), name='vendor-rate-producer'),

]
