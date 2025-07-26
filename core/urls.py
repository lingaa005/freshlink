from django.urls import path
from .views import VendorGroupChatListCreateAPIView


urlpatterns = [
    path('vendor-chat/', VendorGroupChatListCreateAPIView.as_view(), name='vendor-chat'),
]
