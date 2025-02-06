from django.db import models
from django.contrib.auth import get_user_model
from helpdesk.models import Ticket


User = get_user_model()


class SupportRequest(models.Model):
    """Обращение в поддержку."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок обращения"
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=1000
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Тикет"
    )

    def __str__(self):
        return f"Запрос {self.id}: {self.title}"
