from rest_framework.serializers import ModelSerializer, ValidationError
from support.models import SupportRequest
from helpdesk.models import Ticket, Queue


class SupportRequestSerializer(ModelSerializer):
    """API Обращения в поддержку."""

    class Meta:
        model = SupportRequest
        fields = ('user', 'title', 'description', 'created_at', 'ticket')
        read_only_fields = ('ticket',)

    def create(self, validated_data):
        """Создаём тикет при создании обращения."""

        queue = Queue.objects.first()

        if not queue:
            raise ValidationError("Очередь не найдена!")

        ticket = Ticket.objects.create(
            title=validated_data["title"],
            queue=queue,
            submitter_email=validated_data["user"].email,
            description=validated_data["description"],
        )

        validated_data["ticket"] = ticket

        return super().create(validated_data)
