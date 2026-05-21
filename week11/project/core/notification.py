from core.event_bus import subscribe


def send_notification(data):
    print("[NOTIFICATION]")
    print(f"User enrolled/payment success for course {data['course_id']}")


subscribe("PAYMENT_SUCCESS", send_notification)
subscribe("USER_ENROLLED", send_notification)
