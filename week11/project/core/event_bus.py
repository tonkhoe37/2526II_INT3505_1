listeners = {}


def subscribe(event, func):
    if event not in listeners:
        listeners[event] = []
    listeners[event].append(func)


def publish(event, data):
    print(f"\n[EVENT]: {event}")

    if event in listeners:
        for func in listeners[event]:
            func(data)
