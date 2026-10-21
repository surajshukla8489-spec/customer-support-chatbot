# Python Customer Support Chatbot 🤖

A simple Python-based Customer Support Chatbot that answers frequently asked questions, recognizes greetings, checks order status, and provides order cancellation information using JSON files.

## 🚀 Features

- **Greeting Detection:** Responds to greetings like Hello, Hi, and Hey.
- **FAQ Matching:** Answers frequently asked questions using `sample_faq.json`.
- **Order Status Tracking:** Checks order status using an Order ID.
- **Order ID Validation:** Validates the format of order IDs.
- **Cancellation Information:** Checks whether an order is eligible for cancellation.
- **JSON Data Storage:** Stores FAQs and sample order information in JSON files.
- **Help Command:** Displays available chatbot commands.
- **Beginner-Friendly:** Built using core Python concepts.

## 🛠️ Technologies Used

- Python
- JSON
- Regular Expressions (`re`)
- File Handling
- String Processing

## 📁 Project Structure

```text
customer-support-chatbot/
│
├── chatbot.py
├── sample_faq.json
├── orders.json
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/customer-support-chatbot.git
```

### 2. Open the Project Folder

```bash
cd customer-support-chatbot
```

### 3. Run the Chatbot

Make sure Python 3 is installed on your computer.

```bash
python chatbot.py
```

On some systems, you may need to use:

```bash
python3 chatbot.py
```

## 💬 Example Usage

```text
Customer Support Chatbot
Type 'help' to see available commands.
Type 'exit' to quit.

You: Hello
Bot: Hello! Welcome to Customer Support.

You: What are your hours of operation?
Bot: We operate Monday through Friday from 9:00 AM to 6:00 PM IST.

You: Check order ORD1001
Bot: Your order status is Processing.

You: help
Bot: Available commands include FAQs, order status checks, and exit.
```

*Note: Actual responses depend on the implementation and the data stored in your JSON files.*

## 📦 Data Files

### `sample_faq.json`

Contains greeting keywords and frequently asked questions with their answers.

### `orders.json`

Contains sample order records, including order IDs, order statuses, and cancellation eligibility.

**Important:** The included order records are for demonstration purposes only. Cancellation eligibility is informational; the project does not actually cancel orders.

## 🔮 Future Improvements

- Integrate a Django REST Framework API.
- Store customer and order information in a database.
- Add a web interface using React.
- Implement user authentication.
- Integrate an AI-based response system.
- Connect to a real order management system.

## 🎯 Project Objective

The objective of this project is to demonstrate Python programming, JSON file handling, input validation, basic text matching, and customer support automation.

## 👨‍💻 Author

Suraj Shukla

Python Full Stack Developer (Fresher)

## 📄 License

This project is available for learning and educational purposes. Add a license file if you want to specify formal reuse and distribution permissions.
