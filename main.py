import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

# --- THE BRAIN'S IDENTITY ---
BOT_PERSONA = """
You are an AI clone of a guy named [Gulshaheer aslam]. 
You are chatting with friends on WhatsApp. 

1. LANGUAGE RULES:
   - If the user speaks English: Reply in casual English (use slang like "idk", "lol", "brb"), Dont overuse slang, only sometimes.
   - If the user speaks Urdu/Hindi: Reply in **Roman Urdu** (e.g., "kya haal hai", "han yar", "theek hun").
   - If the user uses a mix: Match their energy.

2. TONE & STYLE:
   - Keep it short , can be long if required.
   - Use lowercase mostly (it looks more real).
   - Do not be too enthusiastic. Be chill.
   - Do NOT use proper punctuation like periods at the end.
   - Use emojis rarely, only if it fits.

3. KNOWLEDGE:
   - You know have in depth  knowledge about Coding,Web series,Movies,Games, Cricket and Animes.
   - You love [Cricket, Gaming, Movies,Animes,Coding].
   - If someone asks to call, say you can't right now.

4. GOAL:
   - Reply naturally so they don't realize you are a bot immediately.
"""

# 1. Load the secrets
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: Could not find API key in secrets.env")
else:
    print("✅ Key found! Connecting to Gemini...")
    client = genai.Client(api_key=api_key)
    
    # Disable Safety Filters
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    # Use the STABLE flash model
    generate_config = types.GenerateContentConfig(
        safety_settings=safety_settings

    )

# --- MEMORY STORAGE ---
# Global dictionary to remember context: { "Friend Name": "History..." }
conversation_history = {}

# --- UPDATED BRAIN FUNCTION ---
def get_ai_reply(friend_name, incoming_text):
    try:
        # 1. Retrieve previous history (or start empty)
        past_context = conversation_history.get(friend_name, "")
        
        # 2. Add the new message to history
        updated_context = f"{past_context}\nFriend: {incoming_text}"
        
        # 3. Create prompt with FULL context
        full_prompt = f"{BOT_PERSONA}\n\nCONVERSATION HISTORY:\n{updated_context}\n\nMY REPLY:"
        
        # 4. Ask Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=generate_config
        )
        ai_reply = response.text.strip()
        
        # 5. Save the interaction back to memory
        conversation_history[friend_name] = f"{updated_context}\nMe: {ai_reply}"
        
        return ai_reply
        
    except Exception as e:
        if "429" in str(e):
            print("⏳ Brain tired. Sleeping 60s...")
            time.sleep(60)
            return get_ai_reply(friend_name, incoming_text)
        print(f"Brain Error: {e}")
        return "han bad me bat krta hun"

def setup_browser():
    print("🚀 Launching Browser...")
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={os.getcwd()}/User_Data')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    return driver

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    driver = setup_browser()
    
    print("🤖 Bot is listening... (Press Ctrl+C to stop)")
    # Change this from a string to a dictionary to track multiple chats
    last_processed_msgs = {} 

    try:
        while True:
            # 1. Search for badges in the Side Pane
            unread_badges = driver.find_elements(By.XPATH, '//div[@id="pane-side"]//span[contains(@aria-label, "unread")]')
            
            if unread_badges:
                print("📩 New message detected!")
                
                # --- OFFSET CLICK LOGIC ---
                try:
                    badge = unread_badges[0]
                    action = ActionChains(driver)
                    action.move_to_element(badge).move_by_offset(-50, 0).click().perform()
                except Exception as e:
                    print(f"Click error, trying JS click...")
                    driver.execute_script("arguments[0].click();", unread_badges[0])
                
                # Wait for chat to open
                time.sleep(3) 
                
                # --- SAFETY CHECK: DID IT OPEN? ---
                try:
                    driver.find_element(By.ID, "main")
                except:
                    print("⚠️ Click failed. Chat didn't open. Retrying...")
                    time.sleep(2)
                    continue 

                # --- GROUP DETECTION & NAME EXTRACTION ---
                current_chat_name = "Unknown" 
                
                try:
                    main_header = driver.find_element(By.XPATH, '//div[@id="main"]//header')
                    header_text = main_header.text
                    current_chat_name = header_text.splitlines()[0]
                    
                    print(f"🧐 Checking Chat Header: '{current_chat_name}'")

                    if "," in header_text or " group" in header_text.lower():
                        print(f"🚫 Group detected! Skipping reply.")
                        time.sleep(2)
                        continue 
                        
                except Exception as e:
                    print(f"⚠️ Header check failed: {e}")
                    time.sleep(2)
                    continue
              
                # --- READ & REPLY (Wrapped in try-except for debugging) ---
                try:
                    time.sleep(3)
                    
                    # Target the 'data-pre-plain-text' attribute
                    all_messages = driver.find_elements(By.XPATH, '//div[@data-pre-plain-text]')
                    
                    if all_messages:
                        last_msg = all_messages[-1]
                        sender_info = last_msg.get_attribute("data-pre-plain-text") 
                        last_msg_text = last_msg.text.strip()
                        
                        is_incoming = current_chat_name in sender_info
                        
                        # Use .get() to check the specific friend's last message
                        if is_incoming and last_msg_text != last_processed_msgs.get(current_chat_name, ""):
                            print(f"👀 New message from {current_chat_name} detected!")
                            
                            # Grab up to 5 messages for better context
                            recent_messages = all_messages[-5:]
                            
                            # Build context block with proper sender labels
                            formatted_context = []
                            for m in recent_messages:
                                text = m.text.strip()
                                if not text: continue
                                
                                m_sender_info = m.get_attribute("data-pre-plain-text")
                                if m_sender_info and current_chat_name in m_sender_info:
                                    formatted_context.append(f"Friend: {text}")
                                else:
                                    formatted_context.append(f"Me: {text}")
                                    
                            combined_text = "\n".join(formatted_context)
                            
                            print(f"📜 Context read:\n{combined_text}")
                            print("Thinking...")
                            
                            reply = get_ai_reply(current_chat_name, combined_text)
                            print(f"🧠 Me: {reply}")
                            
                            input_box = driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[@contenteditable="true"]')
                            input_box.click()
                            
                            # FIX FOR SPAMMING: Split by newlines and use Shift+Enter
                            lines = reply.split('\n')
                            for i, line in enumerate(lines):
                                input_box.send_keys(line)
                                if i < len(lines) - 1:
                                    # Shift+Enter adds a new line in WhatsApp without sending
                                    action = ActionChains(driver)
                                    action.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                                    
                            time.sleep(2)
                            input_box.send_keys(Keys.ENTER)
                            print("✅ Reply sent!")

                            # Update Memory for this specific friend
                            last_processed_msgs[current_chat_name] = last_msg_text 

                            print("🔄 Refreshing page to close chat...")
                            time.sleep(2) 
                            driver.refresh()
                            time.sleep(10)
                            
                        else:
                            print("Last message was from me, or already replied. Refreshing...")
                            driver.refresh()
                            time.sleep(5)
                    else:
                        print("⚠️ Could not find 'data-pre-plain-text'. The chat might still be loading...")
                        driver.refresh()
                        time.sleep(5)

                except Exception as loop_error:
                    print(f"❌ Error during read/reply phase: {loop_error}")
                    driver.refresh()
                    time.sleep(5)
               

    except KeyboardInterrupt:
        print("🛑 Stopped.")