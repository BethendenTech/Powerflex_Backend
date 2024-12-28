from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ, Content
from .serializers import FAQSerializer, ContentSerializer


class FAQListView(APIView):
    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContentDetailView(APIView):
    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")  # Get 'code' from URL parameters if passed
        if not code:
            return Response(
                {"error": "Code parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Use get() to fetch a single object
            content = Content.objects.get(code=code)
        except Content.DoesNotExist:
            return Response(
                {"error": "Content not found with the given code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the single object
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
