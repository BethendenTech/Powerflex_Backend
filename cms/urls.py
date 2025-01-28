from django.urls import path
from .views import FAQListView, ContentDetailView

urlpatterns = [
    path("faqs/", FAQListView.as_view(), name="faq-list"),
    path("content/<str:code>/", ContentDetailView.as_view(), name="content-detail"),
]
