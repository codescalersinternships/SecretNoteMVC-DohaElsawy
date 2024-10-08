import os
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from note.ratelimit import RateLimit, RateLimitExceeded
from .models import Note
import cryptocode
from dotenv import load_dotenv

# Create your views here.


show_url = "http://127.0.0.1:8000/note/show/"
err_wrong_http_method = "error, the http mothed is not post"
err_message_readed_or_404 = "the message has been readed or not exist"
err_message_expired = "message has expired"


def create_note(request):

    if request.method != "POST":
        return HttpResponse(err_wrong_http_method)

    content = request.headers["content"]

    encrypted_content = encrypt_content(content)

    note = Note.objects.create(content=encrypted_content)

    url_key = str(note.key) + get_random_string(8)
    note.url_key = url_key
    note.save()

    return HttpResponse(make_secure_url(note.url_key))


def show_note(request, url_key):
    try:
        note = Note.objects.get(url_key=url_key)

        # try:
        #     RateLimit(
        #         key=f"{url_key}:panel:{note.url_key}", limit=1,period=120,
        #     ).check()

        # except RateLimitExceeded as e:
        #     return HttpResponse(f"Rate limit exceeded. You have used {e.usage} requests, limit is {e.limit}.",
        #         status=429,
        #     )

        if is_expiry_date(note.start_date):
            return HttpResponse(err_message_expired)

        decrypted_content = decrypt_contnet(note.content)

        Note.objects.filter(url_key=url_key).delete()
        return HttpResponse(decrypted_content)

    except Note.DoesNotExist:
        return HttpResponse(err_message_readed_or_404)


def make_secure_url(note_url):
    return show_url + note_url


def is_expiry_date(date):
    now = timezone.now()
    duration = now - date

    if (duration.total_seconds() / 3600) > 24:
        return True

    return False


def encrypt_content(content):
    SECRET_KEY = os.environ.get("ENCRYPTKEY")
    encrypted_content = cryptocode.encrypt(content, SECRET_KEY)
    return encrypted_content


def decrypt_contnet(encrypted_content):
    SECRET_KEY = os.environ.get("ENCRYPTKEY")
    content = cryptocode.decrypt(encrypted_content, SECRET_KEY)
    return content
