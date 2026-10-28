from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import UserProfile, Category, Ticket, AuditLog, Comment, InternalNote


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

    def test_technician_can_edit_ticket_priority(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        response = self.client.post(
            reverse('edit_ticket_priority', args=[self.ticket.id]),
            {"priority": "High"}
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.priority, "High")

    def test_technician_cannot_set_invalid_priority(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        original_priority = self.ticket.priority

        response = self.client.post(
            reverse('edit_ticket_priority', args=[self.ticket.id]),
            {"priority": "Emergency"}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.priority, original_priority)

    def test_regular_user_cannot_edit_ticket_priority(self):
        self.client.login(
            username='detail_other',
            password='testpass123'
        )

        original_priority = self.ticket.priority

        response = self.client.post(
            reverse('edit_ticket_priority', args=[self.ticket.id]),
            {"priority": "High"}
        )

        self.assertEqual(response.status_code, 403)

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.priority, original_priority)

    def test_administrator_cannot_edit_ticket_priority(self):
        self.client.login(
            username='detail_admin',
            password='testpass123'
        )

        original_priority = self.ticket.priority

        response = self.client.post(
            reverse('edit_ticket_priority', args=[self.ticket.id]),
            {"priority": "High"}
        )

        self.assertEqual(response.status_code, 403)
        
        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.priority, original_priority)

    def test_technician_can_edit_ticket_category(self):
        active_category = Category.objects.create(
            category_name="Software",
            category_status=True
        )

        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        response = self.client.post(
            reverse('edit_ticket_category', args=[self.ticket.id]),
            {"category": active_category.id}
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.category, active_category)

    def test_technician_cannot_set_inactive_category(self):
        inactive_category = Category.objects.create(
            category_name="Retired Category",
            category_status=False
        )

        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        original_category = self.ticket.category

        response = self.client.post(
            reverse('edit_ticket_category', args=[self.ticket.id]),
            {"category": inactive_category.id}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.ticket.category, original_category)

    def test_regular_user_cannot_edit_ticket_category(self):
        active_category = Category.objects.create(
            category_name="Software",
            category_status=True
        )
        
        self.client.login(
            username='detail_other',
            password='testpass123'
        )

        original_category = self.ticket.category

        response = self.client.post(
            reverse('edit_ticket_category', args=[self.ticket.id]),
            {"category": active_category.id}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.ticket.category, original_category)

    def test_administrator_cannot_edit_ticket_category(self):
        active_category = Category.objects.create(
            category_name="Software",
            category_status=True
        )
        
        self.client.login(
            username='detail_admin',
            password='testpass123'
        )

        original_category = self.ticket.category

        response = self.client.post(
            reverse('edit_ticket_category', args=[self.ticket.id]),
            {"category": active_category.id}
        )

        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.ticket.category, original_category)

    def test_technician_can_add_internal_note(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        response = self.client.post(
            reverse('add_internal_note', args=[self.ticket.id]),
            {"note_text": "Restarted print spooler"}
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            InternalNote.objects.filter(
                ticket=self.ticket,
                author=self.technician,
                note_text="Restarted print spooler"
            ).exists()
        )

    def test_whitespace_does_not_create_internal_note(self):
        self.client.login(
            username='detail_technician',
            password='testpass123'
        )

        response = self.client.post(
            reverse('add_internal_note', args=[self.ticket.id]),
            {"note_text": " "}
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            InternalNote.objects.filter(
                ticket=self.ticket
            ).exists()
        )

    def test_administrator_cannot_add_internal_note(self):
        self.client.login(
            username='detail_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse('add_internal_note', args=[self.ticket.id]),
            {"note_text": "Admin Test Internal Note"}
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            InternalNote.objects.filter(
                ticket=self.ticket
            ).exists()
        )

    def test_regular_user_cannot_add_internal_note(self):
        self.client.login(
            username='detail_other',
            password='testpass123'
        )

        response = self.client.post(
            reverse('add_internal_note', args=[self.ticket.id]),
            {"note_text": "Regular User Test Internal Note"}
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            InternalNote.objects.filter(
                ticket=self.ticket
            ).exists()
        )

    def test_regular_user_cannot_see_internal_notes(self):
        InternalNote.objects.create(
            ticket=self.ticket,
            author=self.technician,
            note_text="Regular User View Test"
        )

        self.client.login(
            username='detail_owner',
            password='testpass123'
        )

        response = self.client.get(
            reverse('ticket_detail', args=[self.ticket.id])
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(
            response,
            "Regular User View Test"
        )

    def test_resolved_status_sets_resolved_date(self):
        self.ticket.change_status(
            self.technician,
            "Resolved"
        )

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "Resolved"
        )

        self.assertIsNotNone(
            self.ticket.resolved_date
        )

    def test_closed_status_sets_closed_date(self):
        self.ticket.change_status(
            self.technician,
            "Closed"
        )
        
        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "Closed"
        )

        self.assertIsNotNone(
            self.ticket.closed_date
        )

    def test_close_ticket_adds_timestamp(self):
        self.ticket.close_ticket(
            self.technician
        )

        self.ticket.refresh_from_db()

        self.assertIsNotNone(
            self.ticket.closed_date
        )

    def test_ticket_owner_can_reopen_closed_ticket(self):
        self.ticket.status = "Closed"
        self.ticket.save()

        self.client.login(
            username='detail_owner',
            password='testpass123'
        )

        response = self.client.post(
            reverse('reopen_ticket', args=[self.ticket.id])
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "Open"
            )

        self.assertTrue(
            AuditLog.objects.filter(
                ticket=self.ticket,
                action="Ticket reopened"
            ).exists()
        )

    def test_non_owner_cannot_reopen_ticket(self):
        self.ticket.status = "Closed"
        self.ticket.save()

        self.client.login(
            username='detail_other',
            password='testpass123'
        )

        response = self.client.post(
            reverse('reopen_ticket', args=[self.ticket.id])
        )

        self.assertEqual(response.status_code, 403)

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "Closed"
        )

        self.assertFalse(
            AuditLog.objects.filter(
                ticket=self.ticket,
                action="Ticket reopened"
            ).exists()
        )

    def test_open_ticket_cannot_be_reopened(self):
        self.client.login(
            username='detail_owner',
            password='testpass123'
        )

        response = self.client.post(
            reverse('reopen_ticket', args=[self.ticket.id])
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "Open"
        )

        self.assertFalse(
            AuditLog.objects.filter(
                ticket=self.ticket,
                action="Ticket reopened"
            ).exists()
        )

    def test_reopening_ticket_sets_admin_attention_flag(self):
        self.ticket.status = "Closed"
        self.ticket.save()

        self.ticket.reopen_ticket(self.owner)

        self.ticket.refresh_from_db()

        self.assertTrue(
            self.ticket.requires_admin_attention
        )

class TicketQueueFilterTests(TestCase):
    def setUp(self):
        self.technician = User.objects.create_user(
            username='queue_technician',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.technician,
            role='technician'
        )

        self.owner1 = User.objects.create_user(
            username='queue_owner1',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.owner1,
            role='regular_user'
        )

        self.owner2 = User.objects.create_user(
            username='queue_owner2',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.owner2,
            role='regular_user'
        )

        self.technician1 = User.objects.create_user(
            username='filter_technician1',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.technician1,
            role='technician'
        )

        self.technician2 = User.objects.create_user(
            username='filter_technician2',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.technician2,
            role='technician'
        )

        self.category1 = Category.objects.create(
            category_name='Hardware'
        )

        self.category2 = Category.objects.create(
            category_name='Software'
        )

        self.ticket_a = Ticket.objects.create(
            status = "Open",
            submitted_by=self.owner1,
            category=self.category1,
            title='Ticket A',
            department='Finance',
            assigned_technician = self.technician1
        )

        self.ticket_b = Ticket.objects.create(
            status = "Resolved",
            submitted_by=self.owner2,
            category=self.category1,
            title='Ticket B',
            department='IT',
            assigned_technician = self.technician2
        )

        self.ticket_c = Ticket.objects.create(
            status = "Open",
            submitted_by=self.owner1,
            category=self.category2,
            title='Ticket C',
            department='IT',
            assigned_technician = None
        )

    def test_ticket_queue_filters_by_status(self):
        self.client.login(
            username = "queue_technician",
            password = "testpass123"
        )

        response = self.client.get(
            reverse("ticket_queue"),
            {"status": "Resolved"}
        )

        self.assertEqual(response.status_code, 200)

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_b, tickets)
        self.assertNotIn(self.ticket_a, tickets)
        self.assertNotIn(self.ticket_c, tickets)

    def test_ticket_queue_filters_by_assignment_state(self):
        self.client.login(
            username='queue_technician',
            password='testpass123'
        )

        response = self.client.get(
            reverse("ticket_queue"),
            {"assignment": "unassigned"}
        )

        self.assertEqual(response.status_code, 200)

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_c, tickets)
        self.assertNotIn(self.ticket_a, tickets)
        self.assertNotIn(self.ticket_b, tickets)

    def test_ticket_queue_combines_filters(self):
        self.client.login(
            username = "queue_technician",
            password = "testpass123"
        )

        response = self.client.get(
            reverse("ticket_queue"),
            {
                "status": "Open",
                "department": "IT"
            }
        )

        self.assertEqual(response.status_code, 200)

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_c, tickets)
        self.assertNotIn(self.ticket_a, tickets)
        self.assertNotIn(self.ticket_b, tickets)

    def test_ticket_queue_filters_by_ticket_number(self):
        self.client.login(
            username = "queue_technician",
            password = "testpass123"
        )

        response = self.client.get(
            reverse("ticket_queue"),
            {"ticket_number": self.ticket_a.id}
        )

        self.assertEqual(response.status_code, 200)

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_a, tickets)
        self.assertNotIn(self.ticket_c, tickets)
        self.assertNotIn(self.ticket_b, tickets)

class ClosedTicketHistoryTests(TestCase):
    def setUp(self):
        self.technician = User.objects.create_user(
            username='history_technician',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.technician,
            role='technician'
        )

        self.admin = User.objects.create_user(
            username='history_admin',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.admin,
            role='administrator'
        )

        self.regular_user = User.objects.create_user(
            username='history_user',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.regular_user,
            role='regular_user'
        )

        self.category = Category.objects.create(
            category_name='Hardware'
        )

        self.ticket_o = Ticket.objects.create(
            status = "Open",
            submitted_by=self.regular_user,
            category=self.category,
            title='Open History Test',
            department='Finance',
            assigned_technician = self.technician
        )

        self.ticket_c = Ticket.objects.create(
            status = "Closed",
            closed_date=timezone.now(),
            submitted_by=self.regular_user,
            category=self.category,
            title='Closed History Test',
            department='IT',
            assigned_technician = self.technician
        )

    def test_technician_can_view_closed_ticket_history(self):
        self.client.login(
            username='history_technician',
            password='testpass123'
        )

        response = self.client.get(
            reverse("closed_ticket_history")
        )

        self.assertEqual(response.status_code, 200)

    def test_administrator_can_view_closed_ticket_history(self):
        self.client.login(
            username='history_admin',
            password='testpass123'
        )

        response = self.client.get(
            reverse("closed_ticket_history")
        )

        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_view_closed_ticket_history(self):
        self.client.login(
            username='history_user',
            password='testpass123'
        )

        response = self.client.get(
            reverse("closed_ticket_history")
        )

        self.assertEqual(response.status_code, 403)

    def test_closed_ticket_history_only_shows_closed_tickets(self):
        self.client.login(
            username='history_technician',
            password='testpass123'
        )

        response = self.client.get(
            reverse("closed_ticket_history")
        )

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_c, tickets)
        self.assertNotIn(self.ticket_o, tickets)

    def test_closed_ticket_history_filters_by_ticket_number(self):
        self.client.login(
            username='history_technician',
            password='testpass123'
        )

        response = self.client.get(
            reverse("closed_ticket_history"),
            {"ticket_number": self.ticket_c.id}
        )

        self.assertEqual(response.status_code, 200)

        tickets = response.context["tickets"]

        self.assertIn(self.ticket_c, tickets)
        self.assertNotIn(self.ticket_o, tickets)

class UserManagementTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='manager_admin',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.admin,
            role='administrator'
        )

        self.target_user = User.objects.create_user(
            username='managed_user',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.target_user,
            role='regular_user'
        )

    def test_admin_can_create_user_with_selected_role(self):
        self.client.login(
            username='manager_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse("user_management"),
            {
                "username": "sasquatch",
                "role": "technician",
                "password1": "daffeyDuck143",
                "password2": "daffeyDuck143"
            }
        )

        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username="sasquatch")

        self.assertEqual(
            new_user.profile.role,
            "technician"
        )

    def test_admin_can_change_user_role(self):
        self.client.login(
            username='manager_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse("change_user_role", args=[self.target_user.id]),
            {
                "role": "technician"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.target_user.profile.refresh_from_db()

        self.assertEqual(
            self.target_user.profile.role,
            "technician"
        )

    def test_admin_can_deactivate_user(self):
        self.client.login(
            username='manager_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse("deactivate_user", args=[self.target_user.id])
        )

        self.assertEqual(response.status_code, 302)

        self.target_user.refresh_from_db()

        self.assertFalse(
            self.target_user.is_active
        )

    def test_admin_cannot_deactivate_themselves(self):
        self.client.login(
            username='manager_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse("deactivate_user", args=[self.admin.id])
        )

        self.assertEqual(response.status_code, 403)

        self.admin.refresh_from_db()

        self.assertTrue(
            self.admin.is_active
        )        

    def test_admin_cannot_change_their_own_role(self):
        self.client.login(
            username='manager_admin',
            password='testpass123'
        )

        response = self.client.post(
            reverse("change_user_role", args=[self.admin.id]),
            {
                "role": "regular_user"
            }
        )

        self.assertEqual(response.status_code, 403)

        self.admin.profile.refresh_from_db()

        self.assertEqual(
            self.admin.profile.role,
            "administrator"
        )

    def test_regular_user_cannot_access_user_management(self):
        self.client.login(
            username = 'managed_user',
            password = 'testpass123'
        )

        response = self.client.get(
            reverse("user_management")
        )

        self.assertEqual(response.status_code, 403)    