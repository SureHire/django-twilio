from functools import wraps
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from twilio.request_validator import RequestValidator

def twilio_signed(view_func):
    @csrf_exempt
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        signature = request.headers.get("X-Twilio-Signature", "") or request.META.get("HTTP_X_TWILIO_SIGNATURE", "")
        url = request.build_absolute_uri()
        body = request.body

        auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
        if not auth_token:
            return HttpResponseForbidden("TWILIO_AUTH_TOKEN not configured.")

        validator = RequestValidator(auth_token)
        if not validator.validate(url, body, signature):
            return HttpResponseForbidden("Invalid Twilio signature.")
        return view_func(request, *args, **kwargs)
    return _wrapped
