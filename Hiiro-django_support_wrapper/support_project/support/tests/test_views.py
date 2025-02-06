from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from support.models import SupportRequest, User
from helpdesk.models import Ticket, Queue


class SupportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test",
            password="qwerty123"
        )
        self.client.force_authenticate(user=self.user)

        self.queue = Queue.objects.create(title="Техподдержка", slug="general")

        self.valid_payload = {
            "title": "Тест",
            "description": "Есть проблема",
            "user": self.user.id
        }

    def test_create_ticket_success(self):
        """Тест успешного создания тикета"""

        response = self.client.post(
            reverse("supportrequest-list"),
            self.valid_payload,
            format="json"
        )

        self.assertEqual(
            response.status_code, 201, "Статус код != 201"
        )
        self.assertTrue(
            SupportRequest.objects.exists(),
            "Отсутствует обращение в поддержку!"
        )
        self.assertTrue(
            Ticket.objects.exists(),
            "Тикер не создан!"
        )
