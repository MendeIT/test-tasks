from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from support.models import SupportRequest
from support.serializers import SupportRequestSerializer


class SupportRequestViewSet(ModelViewSet):
    """API для работы с обращениями в поддержку."""
    queryset = SupportRequest.objects.all().order_by('-created_at')
    serializer_class = SupportRequestSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        """Привязываем пользователя при создании."""
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
