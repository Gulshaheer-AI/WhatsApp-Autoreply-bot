import os
from dotenv import load_dotenv
import google.generativeai as genai
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
    genai.configure(api_key=api_key)
    
    # Disable Safety Filters
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    # Use the STABLE flash model
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash-preview-09-2025',
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
        response = model.generate_content(full_prompt)
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
    last_processed_msg = "" 

    try:
        while True:
            # 1. Search for badges in the Side Pane
            unread_badges = driver.find_elements(By.XPATH, '//div[@id="pane-side"]//span[contains(@aria-label, "unread")]')
            
            if unread_badges:
                print("📩 New message detected!")
                
                # --- OFFSET CLICK LOGIC (Preserved) ---
                try:
                    badge = unread_badges[0]
                    # Move mouse to the badge, then shift 50 pixels to the LEFT, then click
                    action = ActionChains(driver)
                    action.move_to_element(badge).move_by_offset(-50, 0).click().perform()
                except Exception as e:
                    print(f"Click error: {e}")
                    # Backup: Try JS click
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
                # Default name if extraction fails
                current_chat_name = "Unknown" 
                
                try:
                    main_header = driver.find_element(By.XPATH, '//div[@id="main"]//header')
                    header_text = main_header.text
                    
                    # EXTRACT NAME: Take the first line (ignores 'online' status)
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
                
                # --- READ & REPLY ---
                incoming_messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in span.selectable-text")
                
                if incoming_messages:
                    # 1. Check the very last message to see if it's new
                    last_msg_text = incoming_messages[-1].text
                    
                    if last_msg_text != last_processed_msg:
                        print(f"👀 New conversation detected...")
                        
                        # 2. BATCH READ: Grab the last 3 messages instead of just 1
                        # This catches "Suggest a movie" + "Horror" sent together
                        # [-3:] means "The last 3 items in the list"
                        recent_messages = incoming_messages[-3:]
                        
                        # Combine them into one string with newlines
                        combined_text = "\n".join([m.text for m in recent_messages])
                        
                        print(f"📜 Context read: {combined_text}")
                        print("Thinking...")
                        
                        # 3. Send the COMBINED text to the Brain
                        reply = get_ai_reply(current_chat_name, combined_text)
                        print(f"🧠 Me: {reply}")
                        
                        # Type and Send
                        input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                        input_box.click()
                        input_box.send_keys(reply)
                        time.sleep(3)
                        input_box.send_keys(Keys.ENTER)
                        print("✅ Reply sent!")

                        # Update Memory
                        last_processed_msg = last_msg_text 

                        # Refresh Logic
                        print("🔄 Refreshing page to close chat...")
                        time.sleep(2) 
                        driver.refresh()
                        time.sleep(10)
                        
                        continue 
                    else:
                        print("I already replied to this one.")
    except KeyboardInterrupt:
        print("🛑 Stopped.")                    