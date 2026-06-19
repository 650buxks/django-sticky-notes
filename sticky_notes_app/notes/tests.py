from django.test import TestCase
from django.urls import reverse
from .models import StickyNote


class StickyNoteCRUDTests(TestCase):

    def setUp(self):
        """This runs automatically before EVERY test to give us starting data."""
        self.note = StickyNote.objects.create(
            title="Initial Test Note",
            content="This is the starting content."
        )

    def test_read_note(self):
        """1. Test the READ (View) use case"""
        # Assuming your homepage URL name is 'index'
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Check if our dummy note shows up on the page
        self.assertContains(response, "Initial Test Note")

    def test_create_note(self):
        """2. Test the CREATE use case"""
        # Assuming your create URL name is 'create_note' (or similar)
        response = self.client.post(reverse('index'), {
            'title': 'Brand New Note',
            'content': 'Testing the creation pipeline.'
        })
        # We started with 1 note from setUp, now we should have 2
        self.assertEqual(StickyNote.objects.count(), 2)
        # Verify the exact note was saved to the database
        self.assertTrue(StickyNote.objects.filter(title='Brand New Note').exists())

    def test_update_note(self):
        """3. Test the UPDATE (Edit) use case"""
        # Assuming your edit URL takes the note ID: 'edit_note'
        response = self.client.post(reverse('edit_note', args=[self.note.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        # Pull the latest data from the test database
        self.note.refresh_from_db()
        # Assert that the changes actually stuck
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated Content')

    def test_delete_note(self):
        """4. Test the DELETE use case"""
        # Assuming your delete URL takes the note ID: 'delete_note'
        response = self.client.post(reverse('delete_note', args=[self.note.id]))
        # The database should now be completely empty
        self.assertEqual(StickyNote.objects.count(), 0)
