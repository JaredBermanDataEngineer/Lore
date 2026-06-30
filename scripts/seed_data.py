import json
import random
from datetime import datetime, timedelta


random.seed(42)

USER_INITIAL_MESSAGES = [
    "Can you help me find a therapist?",
    "I need help with a tricky situation at work.",
    "I just found out I'm failing chemistry!!",
    "My wife wants to take dancing lessons with me but I have dancing anxiety. Help!!!",
]

BOT_FIRST_RESPONSES = [
    "Tell me a little more about the immediate situation",
    "Can you be a little more specific so I can best help you?",
    "Tell me a little more about yourself, start from the beginning"
]

USER_FIRST_RESPONSES = [
    "I don't know what to say, I feel like I need professional help",
    "I can't get my thoughts straight",
    "Basically my problem started last year, and it's been getting worse",
]

BOT_SECOND_RESPONSES = [
    "OK I recommend Dr. John Doe. Here's a link to his profile: <link>",
    "Got it. I just have a few more quick questions to ask and then I'll get you on your way.",
]

USER_SECOND_RESPONSES = [
    "Thanks so much for the help! I love the product!",
    "What?! No way! Worst app ever!"
]


def random_timestamp(start):
    return (start - timedelta(days=random.randint(5, 60)))


def generate_conversation(customer_id):
    conversation = {
        "customer_id": customer_id,
        "messages": []
    }

    # First user message
    timestamp = random_timestamp(datetime.now())
    conversation["messages"].append({
        "role": "user",
        "timestamp": timestamp.isoformat(),
        "content": random.choice(USER_INITIAL_MESSAGES)
    })

    # First assistant message
    timestamp += timedelta(seconds=random.randint(1, 5))
    conversation["messages"].append({
        "role": "assistant",
        "timestamp": timestamp.isoformat(),
        "content": random.choice(BOT_FIRST_RESPONSES)
    })

    # First user response
    timestamp += timedelta(seconds=random.randint(5, 300))
    conversation["messages"].append({
        "role": "user",
        "timestamp": timestamp.isoformat(),
        "content": random.choice(USER_FIRST_RESPONSES)
    })

    # Second assistant message
    timestamp += timedelta(seconds=random.randint(5, 600))
    conversation["messages"].append({
        "role": "assistant",
        "timestamp": timestamp.isoformat(),
        "content": random.choice(BOT_SECOND_RESPONSES)
    })

    # Second user response
    timestamp += timedelta(seconds=random.randint(5, 600))
    conversation["messages"].append({
        "role": "user",
        "timestamp": timestamp.isoformat(),
        "content": random.choice(USER_SECOND_RESPONSES)
    })

    return conversation


def generate_dataset(num_conversations):
    return [
        generate_conversation(i + 1)
        for i in range(num_conversations)
    ]


if __name__ == "__main__":
    dataset = generate_dataset(5)

    with open("data/chats.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
