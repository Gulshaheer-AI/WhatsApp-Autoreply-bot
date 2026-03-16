# 🤖 WhatsApp Autoresponder Bot

An automated, persona-driven WhatsApp bot built with Python, Selenium, and Google's Gemini AI. 

This script automates WhatsApp Web to act as a digital clone of the user. It detects unread messages, maintains short-term conversational memory, and generates context-aware, human-like responses in English or Roman Urdu, seamlessly mimicking casual texting styles.

## 🚀 Key Features
* **Web Automation:** Uses Selenium WebDriver to navigate WhatsApp Web, detect unread message badges, and interact with the DOM to read and send messages.
* **Contextual Memory:** Maintains a localized dictionary to track recent conversation history for individual users, allowing Gemini to understand the flow of the chat.
* **Persona Engineering:** The LLM is strictly prompted to reply with casual syntax (lowercase, minimal punctuation, occasional slang) to avoid sounding robotic.
* **Smart Filtering:** Automatically detects and ignores Group Chats to prevent accidental spamming.
* **Dynamic Content Batching:** Reads the last several messages at once to capture split-sentence texting habits.

## 🛠️ Technology Stack
| Component | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.x |
| **Browser Automation** | Selenium, Webdriver Manager |
| **AI Engine** | Google Generative AI (`gemini-2.5-flash-preview`) |
| **Environment** | `python-dotenv` |

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Gulshaheer-AI/WhatsApp-Autoreply-bot.git](https://github.com/Gulshaheer-AI/WhatsApp-Autoreply-bot.git)
cd WhatsApp-Autoreply-bot
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure the Environment
Create a `.env` file in the root directory to store your API key safely. **Do not upload this file to GitHub!**
```text
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Bot
```bash
python main.py
```
*Note: On the first run, a Chrome window will open asking you to scan the WhatsApp Web QR code with your phone. Subsequent runs will use the locally saved `User_Data` profile to bypass login.*

## 🚧 Known Limitations & Future Roadmap
This is an MVP (Minimum Viable Product) and is actively being refined. Current focus areas include:
* **Media Handling:** The bot currently parses only text. It cannot process or generate images, stickers, or voice notes.
* **Message Pacing:** Occasional rapid-fire message reading can lead to bundled or slightly delayed responses (e.g., sending multiple messages at once).
* **Headless Execution:** Future iterations will aim to run the browser entirely in the background.

## 👨‍💻 Author
**Gulshaheer Aslam**
* AI & Backend Development Student
* [LinkedIn](www.linkedin.com/in/gulshaheer-aslam-195445254)
