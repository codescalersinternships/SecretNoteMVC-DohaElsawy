import os
from django.utils import timezone
from django.http import HttpResponse
from django.utils.crypto import get_random_string

from note.ratelimit import RateLimit, RateLimitExceeded

from .models import Note
import cryptocode

# Create your views here.


show_url = "http://127.0.0.1:8000/note/show/"
err_wrong_http_method = "error, the http mothed is not post"
err_message_readed_or_404 = "the message has been readed or not exist"
err_message_expired = "message has expired"
err_block_request = "you reach request's limit, please wait 1 min"
RATE_LIMIT = 5
PERIOD = 60


def create_note(request):

    if request.method != "POST":
        return HttpResponse(err_wrong_http_method, status=405)

    content = request.headers["content"]

    encrypted_content = encrypt_content(content)

    note = Note.objects.create(content=encrypted_content)

    url_key = str(note.key) + get_random_string(8)
    note.url_key = url_key
    note.save()

    return HttpResponse(make_secure_url(note.url_key), status=200)


def show_note(request, url_key):
    try:

        try:
            RateLimit(
                key=f"{'127.0.0.1'}:panel:{'127.0.0.1'}",
                limit=RATE_LIMIT,
                period=PERIOD,
            ).check()
        except RateLimitExceeded as e:
            return HttpResponse(
                err_block_request,
                status=429,
            )

        note = Note.objects.get(url_key=url_key)

        if is_expiry_date(note.start_date):
            return HttpResponse(err_message_expired, status=410)

        decrypted_content = decrypt_contnet(note.content)

        Note.objects.filter(url_key=url_key).delete()
        return HttpResponse(decrypted_content, status=200)

    except Note.DoesNotExist:
        return HttpResponse(err_message_readed_or_404, status=404)


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
