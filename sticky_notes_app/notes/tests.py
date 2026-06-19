from django.test import TestCase
from django.urls import reverse
from .models import StickyNote


class StickyNoteModelTest(TestCase):
    def setUp(self):
        # Create a sample sticky note in the temporary test database
        StickyNote.objects.create(
            title="Study Milestones",
            content="Complete Level 1 and Level 2 Django benchmarks."
        )

    def test_note_has_title(self):
        """Test that a StickyNote object holds its expected title data"""
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.title, "Study Milestones")

    def test_note_has_content(self):
        """Test that a StickyNote object holds its expected text content"""
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.content, "Complete Level 1 and Level 2 Django benchmarks.")


class StickyNoteViewTest(TestCase):
    def setUp(self):
        # Set up a sample note to verify view rendering pipelines
        StickyNote.objects.create(
            title="Gym Protocol",
            content="Focus on heavy triples using RPE targeting."
        )

    def test_index_view_status_and_content(self):
        """Test that the homepage loads successfully and displays notes"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gym Protocol")
        self.assertContains(response, "Focus on heavy triples using RPE targeting.")

    def test_edit_view_status(self):
        """Test that the edit view screen successfully loads
        for a specific note"""
        note = StickyNote.objects.get(id=1)
        response = self.client.get(reverse('edit_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
