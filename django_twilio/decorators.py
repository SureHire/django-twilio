from functools import wraps
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

from .utils import get_blacklisted_response

ALLOWED_METHODS = ('GET', 'POST')

def twilio_signed(view_func):
    """
    Decorator to validate Twilio requests using the X-Twilio-Signature header.
    Compatible with twilio-python RequestValidator.
    """

    @csrf_exempt
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        # Determine if we should enforce forgery protection
        use_forgery_protection = getattr(
            settings,
            "DJANGO_TWILIO_FORGERY_PROTECTION",
            not getattr(settings, "DEBUG", False),
        )

        # Only validate for GET/POST
        if use_forgery_protection:
            if request.method not in ALLOWED_METHODS:
                return HttpResponseNotAllowed(ALLOWED_METHODS)

            signature = (
                request.headers.get("X-Twilio-Signature")
                or request.META.get("HTTP_X_TWILIO_SIGNATURE", "")
            )
            if not signature:
                return HttpResponseForbidden("Missing Twilio signature.")

            auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
            if not auth_token:
                return HttpResponseForbidden("TWILIO_AUTH_TOKEN not configured.")

            validator = RequestValidator(auth_token)
            url = request.build_absolute_uri()

            # Decide which data to validate
            data = request.POST if request.method == "POST" else request.GET

            if not validator.validate(url, data, signature):
                return HttpResponseForbidden("Invalid Twilio signature.")

        # Blacklist check
        blacklisted_resp = get_blacklisted_response(request)
        if blacklisted_resp:
            return blacklisted_resp

        # Call the original view
        response = view_func(request, *args, **kwargs)

        # Wrap Twilio Verb objects
        if isinstance(response, VoiceResponse):
            return HttpResponse(str(response), content_type="application/xml")

        # Wrap raw bytes
        if isinstance(response, (bytes, bytearray)):
            return HttpResponse(response, content_type="application/xml")

        # Wrap strings
        if isinstance(response, str):
            return HttpResponse(response, content_type="application/xml")

        # Otherwise return as-is (HttpResponse)
        return response

    return _wrapped

twilio_view = twilio_signed
