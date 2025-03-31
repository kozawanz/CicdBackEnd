from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Note

class NoteAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a test note
        self.note = Note.objects.create(title="Test Note", content="This is a test note.", user=self.user)

    def test_create_note(self):
        """ Test creating a new note """
        data = {"title": "New Note", "content": "This is another test note."}
        response = self.client.post("/api/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notes(self):
        """ Test retrieving notes """
        response = self.client.get("/api/notes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_note(self):
        """ Test updating an existing note """
        data = {"title": "Updated Note", "content": "Updated content."}
        response = self.client.put(f"/api/update/{self.note.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        """ Test deleting a note """
        response = self.client.delete(f"/api/delete/{self.note.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
