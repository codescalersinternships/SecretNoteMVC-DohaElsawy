import datetime
from django.test import TestCase

from note.views import RATE_LIMIT
from .models import Note
import datetime
from django.core.cache import cache

# Create your tests here.


class NoteViewTests(TestCase):
    def setUp(self):
        cache.clear()

    @classmethod
    def setUpTestData(cls):

        Note.objects.create(
            content="test",
            url_key="62515590-782b-4ae7-b091-acbae81f7baepdx9wo3T",
            key="62515590-782b-4ae7-b091-acbae81f7bae",
        )

        Note.objects.create(
            content="test",
            url_key="74789473-782b-4ae7-b091-acbae81f7baepdx9wo3T",
            key="74789473-782b-4ae7-b091-acbae81f7bae",
        )

        note = Note.objects.get(id=2)
        note.start_date = datetime.datetime(2020, 5, 6, 3, 4, 5, 6)
        note.save()

    def test_create_note_success(self):
        response = self.client.post(
            "/note/new/",
            headers={"content": "test"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 76)

    def test_wrong_http_method_create_note(self):
        response = self.client.get(
            "/note/new/",
        )
        self.assertEqual(response.status_code, 405)

    def test_show_note(self):
        note = Note.objects.get(id=1)
        response = self.client.get(
            f"/note/show/{note.url_key}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, None)

    def test__failed_show_note(self):
        response = self.client.get(
            f"/note/show/unkown",
        )
        self.assertEqual(response.status_code, 404)

    def test__expired_show_note(self):
        note = Note.objects.get(id=2)
        response = self.client.get(
            f"/note/show/{note.url_key}",
        )
        self.assertEqual(response.status_code, 410)

    def test_rate_limit_show_note(self):
        notes = []
        for i in range(9):
            notes.append(
                Note.objects.create(
                    content="test",
                    url_key=f"{i}4799473-782b-4ae7-b091-acbae81f7baepdx9wo3T",
                    key=f"{i}4799473-782b-4ae7-b091-acbae81f7bae",
                )
            )
        for i in range(len(notes)):
            response = self.client.get(
                f"/note/show/{notes[i].url_key}",
            )
            if i > RATE_LIMIT:
                self.assertEqual(response.status_code, 429)
                break


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Note.objects.create(
            content="test",
            url_key="62515590-782b-4ae7-b091-acbae81f7baepdx9wo3T",
            key="62515590-782b-4ae7-b091-acbae81f7bae",
        )

    def test_content_label(self):
        note = Note.objects.get(id=1)

        content = note._meta.get_field("content").verbose_name
        self.assertEqual(content, "content")

    def test_url_key_label(self):
        note = Note.objects.get(id=1)

        url_key = note._meta.get_field("url_key").verbose_name
        max_url_key = note._meta.get_field("url_key").max_length

        self.assertEqual(max_url_key, 45)
        self.assertEqual(url_key, "url key")

    def test_key_label(self):
        note = Note.objects.get(id=1)

        key = note._meta.get_field("key").verbose_name
        max_key = note._meta.get_field("key").max_length

        self.assertEqual(max_key, 32)
        self.assertEqual(key, "key")
