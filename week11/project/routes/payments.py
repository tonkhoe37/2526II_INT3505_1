from fastapi import APIRouter
from core.event_bus import publish

router = APIRouter()


@router.post("/webhook/payment")
def payment_webhook(payload: dict):

    print("\n[WEBHOOK RECEIVED]", payload)

    if payload["event"] == "payment.success":

        publish("PAYMENT_SUCCESS", payload)

    return {"status": "ok"}
