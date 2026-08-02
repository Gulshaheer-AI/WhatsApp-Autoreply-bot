# 🤖 WhatsApp Autoresponder Bot

An automated, persona-driven WhatsApp bot built with Python, Selenium, and Google's Gemini AI. 

This script automates WhatsApp Web to act as an AI digital clone of the user. It detects unread messages, maintains multi-recipient conversational memory, accurately attributes chat history, and generates context-aware, human-like responses in English or Roman Urdu.

## 🚀 Key Features

* **Resilient DOM Automation:** Bypasses Meta's dynamic/hashed CSS classes by targeting stable functional attributes (`data-pre-plain-text`), ensuring the bot remains functional through WhatsApp Web UI updates.
* **Isolated Conversational Memory:** Uses per-contact state tracking (`last_processed_msgs`) to manage context for multiple active chats independently without state overwrites.
* **Accurate Speaker Attribution:** Distinguishes between incoming messages (`Friend:`) and previous automated replies (`Me:`), giving Gemini clean, structured multi-turn conversation history.
* **Human-Style Formatting & Anti-Spam:** Utilizes `Shift + Enter` keyboard actions for multi-line AI responses, preventing raw newline characters (`\n`) from triggering rapid-fire premature message sends.
* **Persona Engineering:** Prompts the LLM to reply with casual syntax (lowercase, minimal punctuation, contextual slang) to sound natural and realistic.
* **Smart Filtering:** Automatically detects and skips group chats to prevent accidental automated replies in group settings.

## 🛠️ Technology Stack

| Component | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.x |
| **Browser Automation** | Selenium WebDriver (`ActionChains`, `Keys`), Webdriver Manager |
| **AI Engine** | Google Generative AI (`google-genai` / `gemini-2.5-flash-preview`) |
| **Environment** | `python-dotenv` |

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Gulshaheer-AI/WhatsApp-Autoreply-bot.git
cd WhatsApp-Autoreply-bot
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory to store your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Bot
```bash
python main.py
```
*Note: On the first run, scan the WhatsApp Web QR code in the opened Chrome window. Subsequent runs automatically use the persistent local profile (`User_Data`) to stay logged in.*

## 🚧 Known Limitations & Future Roadmap

This project is continuously evolving. Planned enhancements include:

-  **Agentic AI Integration:** Upgrade from standard prompt wrapping to an agentic framework (e.g., LangGraph) for dynamic tool calling (e.g., checking weather, querying live APIs).
-  **Rich Media Support:** Processing and responding to images, voice notes, and stickers.
-  **Headless Execution:** Running browser background automation seamlessly without an active GUI window.

## 👨‍💻 Author

**Gulshaheer Aslam**  
* AI & Backend Development Student  
* [LinkedIn](https://www.linkedin.com/in/gulshaheer-aslam-195445254)
