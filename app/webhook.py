import hmac
import logging
import os
from django.http import HttpRequest
from ninja import NinjaAPI

from app.hookmodel import PushPayload
from app.tasks import process_forgejo_event
# import app.ebuild_parse

gitapi = NinjaAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

secret_key = os.environ.get("WEBHOOK_SECRET", "")

@gitapi.post("/webhook")
def handle_webhook(request: HttpRequest):
    event_type = request.headers.get("X-Forgejo-Event")
    if event_type != "push":
        logger.info(f"Ignoring unsupported event type: {event_type}")
        return {"status": "ignored"}

    # verify webhook signature
    if not verify_webhook_signature(request, secret_key):
        logger.error("Webhook signature verification failed")
        return {"status": "failed"}

    push_payload = PushPayload.model_validate_json(request.body.decode())
    process_forgejo_event.delay(push_payload.model_dump(mode="json"))


def verify_webhook_signature(request: HttpRequest, secret: str) -> bool:
    signature = request.headers.get("X-Forgejo-Signature")
    if not signature:
        logger.error("No signature found in headers")
        return False

    computed_signature = hmac.new(secret.encode(), request.body, digestmod="sha256").hexdigest()
    if not hmac.compare_digest(computed_signature, signature):
        logger.error("Invalid webhook signature")
        return False

    return True