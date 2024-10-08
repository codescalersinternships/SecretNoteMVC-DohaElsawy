from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from .models import Note

# Create your views here.


show_url = "http://127.0.0.1:8000/note/show/"
err_wrong_http_method = "error, the http mothed is not post"
err_message_readed = "the message has been readed"
err_message_expired = "message has expired"
err_message_404 = "message not found"


def create_note(request):

    if request.method != "POST":
        return HttpResponse(err_wrong_http_method)

    content = request.headers["content"]
    note = Note.objects.create(content=content)
    url = str(note.identifier) + get_random_string(8)
    note.url = url
    note.save()
    return HttpResponse(make_secure_url(note.url))


def show_note(request, url):
    try:
        note = Note.objects.get(url=url)
    except Note.DoesNotExist:
        return HttpResponse(err_message_404)

    if note.is_read == True:
        return HttpResponse(err_message_readed)
    
    if is_expiry_date(note.start_date):
        return HttpResponse(err_message_expired)
    
    note.is_read = True
    note.save()
    return HttpResponse(note.content)


def make_secure_url(note_url):
    return show_url + note_url


def is_expiry_date(date):
    now = timezone.now()
    duration = now - date

    if (duration.total_seconds() / 3600) > 24:
        return True

    return False
