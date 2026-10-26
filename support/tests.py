from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserProfile, Category, Ticket, AuditLog, Comment


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

    def test_anonymous_user_cannot_assign_technician(self):
        response = self.client.post(
            reverse(
                'assign_technician',
                args=[self.ticket.id]
            ),
            {'technician': self.technician.id}
        )

        self.ticket.refresh_from_db()

        self.assertIn(response.status_code, [302, 401, 403])
        self.assertIsNone(self.ticket.assigned_technician)

    def test_administrator_cannot_assign_invalid_technician(self):
        self.client.login(
            username='admin_test',
            password='testpass123'
        )

        response = self.client.post(
            reverse(
                'assign_technician',
                args=[self.ticket.id]
            ),
            {'technician': 999999}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertIsNone(self.ticket.assigned_technician)

    def test_technician_cannot_assign_technician(self):
        self.client.login(
            username='technician_test',
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


class AuthenticationRBACTests(TestCase):

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

    def test_regular_user_can_access_my_tickets(self):
        self.client.login(
            username='regular_test',
            password='testpass123'
        )
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_technician_cannot_access_my_tickets(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_access_my_tickets(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_access_ticket_queue(self):
        self.client.login(
            username='regular_test',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_queue'))
        self.assertEqual(response.status_code, 403)

    def test_technician_can_access_ticket_queue(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_queue'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_ticket_queue(self):
        response = self.client.get(reverse('ticket_queue'))
        self.assertEqual(response.status_code, 302)

    def test_administrator_can_access_ticket_queue(self):
        self.client.login(
            username='admin_test',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_queue'))
        self.assertEqual(response.status_code, 200)

class TechnicianClaimingTests(TestCase):

    def setUp(self):
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

        self.technician_two = User.objects.create_user(
            username='technician_test_two',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.technician_two,
            role='technician'
        )

        self.category = Category.objects.create(
            category_name='Test Category'
        )
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='This is a test ticket.',
            category=self.category,
            submitted_by=self.regular_user,
            affected_device_system='Test Computer',
            priority='Medium',
            department='IT'
        )

    def test_technician_can_claim_unassigned_ticket(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )
        response = self.client.post(reverse('claim_ticket', args=[self.ticket.id]))

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.assigned_technician, self.technician)
        
        self.assertEqual(response.status_code, 302)

    def test_technician_cannot_overwrite_existing_assignment(self):
        self.ticket.assigned_technician = self.technician
        self.ticket.save()

        self.client.login(
            username='technician_test_two',
            password='testpass123'
        )
        response = self.client.post(reverse('claim_ticket', args=[self.ticket.id]))

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.assigned_technician, self.technician)
        
        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_claim_ticket(self):
        self.client.login(
            username='regular_test',
            password='testpass123'
        )
        response = self.client.post(reverse('claim_ticket', args=[self.ticket.id]))

        self.ticket.refresh_from_db()

        self.assertIsNone(self.ticket.assigned_technician)
        
        self.assertEqual(response.status_code, 403)

    def test_GET_request_does_not_claim_ticket(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )
        response = self.client.get(reverse('claim_ticket', args=[self.ticket.id]))

        self.assertEqual(response.status_code, 302)

        self.assertIsNone(self.ticket.assigned_technician)

class CategoryManagementTests(TestCase):

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

        self.category = Category.objects.create(
            category_name='Hardware'
        )

    def test_administrator_can_open_category_management_page(self):
        self.client.login(
            username='admin_test',
            password='testpass123'
        )
        response = self.client.get(reverse('category_management'))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_open_category_management_page(self):
        self.client.login(
            username='regular_test',
            password='testpass123'
        )
        response = self.client.get(reverse('category_management'))
        self.assertEqual(response.status_code, 403)

    def test_administrator_can_add_category(self):
        self.client.login(
            username='admin_test',
            password='testpass123'
        )
        response = self.client.post(reverse('category_management'), {'category_name': 'Software'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(category_name='Software').exists())

    def test_deactivation_toggle(self):
        self.category.category_status = True
        self.category.save()        
        self.client.login(
            username='admin_test',
            password='testpass123'
        )        
        response = self.client.post(reverse('toggle_category_status', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertFalse(self.category.category_status)

    def test_activation_toggle(self):
        self.category.category_status = False
        self.category.save()
        self.client.login(
            username='admin_test',
            password='testpass123'
        )
        response = self.client.post(reverse('toggle_category_status', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertTrue(self.category.category_status)

class AuditLoggingTests(TestCase):

    def setUp(self):
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
            category_name='Test Category'
        )

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='This is a test ticket.',
            category=self.category,
            submitted_by=self.regular_user,
            affected_device_system='Test Computer',
            priority='Medium',
            department='IT'
        )

    def test_audit_log_created_on_ticket_claim(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )

        response = self.client.post(reverse('claim_ticket', args=[self.ticket.id]))

        self.assertEqual(response.status_code, 302)

        log = AuditLog.objects.get(ticket=self.ticket)

        self.assertEqual(log.action, 'Ticket assigned to technician_test')
        self.assertEqual(log.user, self.technician)
        self.assertEqual(log.ticket, self.ticket)
        self.assertIsNotNone(log.timestamp)

    def test_audit_log_created_on_status_change(self):
        self.client.login(
            username='technician_test',
            password='testpass123'
        )
        self.ticket.assigned_technician = self.technician
        self.ticket.save()
        response = self.client.post(reverse('edit_ticket_status', args=[self.ticket.id]), {'status': 'In Progress'})
        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'In Progress')

        log = AuditLog.objects.get(ticket=self.ticket)
        self.assertEqual(log.action, 'Status changed from Open to In Progress')
        self.assertEqual(log.user, self.technician)
        self.assertEqual(log.ticket, self.ticket)
        self.assertIsNotNone(log.timestamp)

    def test_audit_log_created_on_ticket_close(self):
        self.ticket.close_ticket(self.technician)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'Closed')

        log = AuditLog.objects.get(ticket=self.ticket)

        self.assertEqual(log.action, 'Ticket closed')
        self.assertEqual(log.user, self.technician)
        self.assertEqual(log.ticket, self.ticket)
        self.assertIsNotNone(log.timestamp)

class TicketDetailTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='detail_owner',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.owner,
            role='regular_user'
        )

        self.other_user = User.objects.create_user(
            username='detail_other',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.other_user,
            role='regular_user'
        )

        self.technician = User.objects.create_user(
            username='detail_technician',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.technician,
            role='technician'
        )

        self.admin = User.objects.create_user(
            username='detail_admin',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.admin,
            role='administrator'
        )

        self.category = Category.objects.create(
            category_name='Hardware'
        )

        self.ticket = Ticket.objects.create(
            submitted_by=self.owner,
            category=self.category,
            title='Detail Test Ticket',
            affected_device_system='Desktop',
            description='Test detail test',
            priority='Medium',
            department='IT'
        )

    def test_owner_can_view_ticket_detail(self):
        self.client.login(
            username='detail_owner',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)

    def test_other_regular_user_cannot_view_ticket_detail(self):
        self.client.login(
            username='detail_other',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 403)

    def test_technician_can_view_ticket_detail(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)

    def test_administrator_can_view_ticket_detail(self):
        self.client.login(
            username='detail_admin',
            password='testpass123'
        )
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirected_from_ticket_detail(self):
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)

    def test_owner_can_add_comment(self):
        self.client.login(
            username='detail_owner',
            password='testpass123'
        )
        response = self.client.post(
            reverse('ticket_detail', args=[self.ticket.id]),
            {'comment_text': 'Owner comment test.'}
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Comment.objects.filter(
                ticket=self.ticket, 
                author=self.owner, 
                comment_text='Owner comment test.'
                ).exists()
                )

    def test_technician_can_add_comment(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )
        response = self.client.post(
            reverse('ticket_detail', args=[self.ticket.id]),
            {'comment_text': 'Technician comment test.'}
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Comment.objects.filter(
                ticket=self.ticket, 
                author=self.technician, 
                comment_text='Technician comment test.'
                ).exists()
                )

    def test_administrator_can_add_comment(self):
        self.client.login(
            username='detail_admin',
            password='testpass123'
        )
        response = self.client.post(
            reverse('ticket_detail', args=[self.ticket.id]),
            {'comment_text': 'Administrator comment test.'}
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Comment.objects.filter(
                ticket=self.ticket, 
                author=self.admin, 
                comment_text='Administrator comment test.'
                ).exists()
                )

    def test_unauthorized_user_cannot_add_comment(self):
        self.client.login(
            username='detail_other',
            password='testpass123'
        )
        response = self.client.post(
            reverse('ticket_detail', args=[self.ticket.id]),
            {'comment_text': 'Unauthorized comment test.'}
        )
        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Comment.objects.filter(
                ticket=self.ticket, 
                author=self.other_user, 
                comment_text='Unauthorized comment test.'
                ).exists()
                )