
import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "sample_faq.json"
ORDERS_FILE = BASE_DIR / "orders.json"


# Load JSON data safely
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Warning: {file_path.name} not found.")
        return {}

    except json.JSONDecodeError:
        print(f"Error: {file_path.name} contains invalid JSON.")
        return {}


# Normalize user input
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s'-]", " ", text)
    return re.sub(r"\s+", " ", text)


# Check greetings from the JSON dataset
def check_greeting(message, greetings):
    for greeting in greetings:
        pattern = r"(?<!\w)" + re.escape(
            normalize_text(greeting)
        ) + r"(?!\w)"

        if re.search(pattern, message):
            return True

    return False


# Match questions against FAQ dataset
def match_faqs(message, faqs):
    matched = []

    # Helpful alternative phrases for the supplied FAQ questions
    aliases = {
        0: [
            "business hours", "opening hours", "working hours",
            "office timing", "when do you open", "closing time"
        ],
        1: [
            "submit project", "internship project",
            "github link", "project submission",
            "student workspace"
        ],
        2: [
            "certificate", "certificate date",
            "receive certificate", "certificate status",
            "when will i get my certificate"
        ]
    }

    for index, faq in enumerate(faqs):
        question = normalize_text(faq.get("question", ""))

        # Exact question or question phrase match
        if question and question in message:
            matched.append(faq)
            continue

        # Match known alternative phrases
        phrases = aliases.get(index, [])

        found = False
        for phrase in phrases:
            pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"

            if re.search(pattern, message):
                matched.append(faq)
                found = True
                break

        if found:
            continue

        # Match meaningful words from the FAQ question
        stop_words = {
            "what", "are", "your", "how", "do", "i",
            "the", "my", "when", "will", "you", "is",
            "a", "an", "of", "to", "and", "in"
        }

        question_words = {
            word for word in re.findall(r"\b\w+\b", question)
            if len(word) > 2 and word not in stop_words
        }

        message_words = set(re.findall(r"\b\w+\b", message))

        overlap = question_words & message_words

        if len(overlap) >= 2:
            matched.append(faq)

    return matched


# Find order by ID
def find_order(order_id, orders):
    for order in orders:
        if order.get("order_id", "").upper() == order_id.upper():
            return order

    return None


# Handle order status and cancellation
def handle_order(message, orders):
    wants_cancel = bool(
        re.search(r"\b(cancel|cancellation)\b", message)
    )

    wants_status = bool(
        re.search(
            r"\b(track|tracking|status)\b|"
            r"\bwhere is my order\b",
            message
        )
    )

    if not wants_cancel and not wants_status:
        return None

    match = re.search(
        r"\bORD[ -]?\d{4,10}\b",
        message,
        re.IGNORECASE
    )

    if not match:
        return "Please provide your order ID, for example ORD1001."

    order_id = re.sub(r"[ -]", "", match.group()).upper()
    order = find_order(order_id, orders)

    if not order:
        return f"Order {order_id} was not found in our demo records."

    if wants_cancel:
        if order.get("cancellable") is True:
            return (
                f"Order {order_id} is eligible for cancellation "
                "in this demo. No actual cancellation was performed."
            )

        return (
            f"Order {order_id} cannot be cancelled in this demo. "
            f"Current status: {order.get('status', 'Unknown')}."
        )

    return (
        f"Order ID: {order_id}\n"
        f"Status: {order.get('status', 'Unknown')}"
    )


# Generate chatbot response
def generate_response(user_input, dataset, orders):
    message = normalize_text(user_input)

    if not message:
        return "Please enter a question."

    if re.fullmatch(r"(bye|goodbye|exit|quit)", message):
        return "Goodbye! Thank you for contacting support."

    if message == "help":
        return (
            "You can ask about:\n"
            "1. Greetings\n"
            "2. Business hours\n"
            "3. Internship project submission\n"
            "4. Certificate status\n"
            "5. Order status\n"
            "6. Order cancellation\n"
            "Type 'bye' to exit."
        )

    greetings = dataset.get("greetings", [])

    if check_greeting(message, greetings):
        return "Hello! Welcome to customer support. How can I help you?"

    order_response = handle_order(message, orders)

    if order_response is not None:
        return order_response

    faqs = dataset.get("faqs", [])
    matched = match_faqs(message, faqs)

    if matched:
        # Remove duplicate answers while preserving their order
        answers = list(dict.fromkeys(
            faq.get("answer", "Answer unavailable.")
            for faq in matched
        ))

        return "\n".join(answers)

    return (
        "Sorry, I couldn't understand your question.\n"
        "Type 'help' to see available topics."
    )


# Main interactive chatbot
def main():
    dataset = load_json(FAQ_FILE)
    order_data = load_json(ORDERS_FILE)
    orders = order_data.get("orders", [])

    print("=" * 45)
    print("       CUSTOMER SUPPORT CHATBOT")
    print("=" * 45)
    print("Bot: Hello! How can I help you?")
    print("Bot: Type 'help' for topics or 'bye' to exit.")

    while True:
        try:
            user_input = input("\nYou: ")
            message = normalize_text(user_input)

            response = generate_response(
                user_input, dataset, orders
            )

            print("Bot:", response)

            if re.fullmatch(
                r"(bye|goodbye|exit|quit)", message
            ):
                break

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! Have a nice day.")
            break

        except Exception as error:
            print("Bot: Something went wrong. Please try again.")
            print("Error details:", error)


if __name__ == "__main__":
    main()
