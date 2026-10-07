from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserProfile, Category, Ticket


class TechnicianAssignmentTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_test',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.admin,
            role='administrator'
        )

        self.regular_user = User.objects.create_user(
            username='regular_test',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.regular_user,
            role='regular_user'
        )

        self.technician = User.objects.create_user(
            username='technician_test',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.technician,
            role='technician'
        )

        self.category = Category.objects.create(
            category_name='Hardware'
        )

        self.ticket = Ticket.objects.create(
            submitted_by=self.regular_user,
            category=self.category,
            title='Test Ticket',
            affected_device_system='Test Computer',
            description='Test description',
            priority='Medium',
            department='IT'
        )

    def test_administrator_can_assign_technician(self):
        self.client.login(
            username='admin_test',
            password='testpass123'
        )

        response = self.client.post(
            reverse(
                'assign_technician',
                args=[self.ticket.id]
            ),
            {'technician': self.technician.id}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.ticket.assigned_technician,
            self.technician
        )

    def test_regular_user_cannot_assign_technician(self):
        self.client.login(
            username='regular_test',
            password='testpass123'
        )

        response = self.client.post(
            reverse(
                'assign_technician',
                args=[self.ticket.id]
            ),
            {'technician': self.technician.id}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertIsNone(self.ticket.assigned_technician)