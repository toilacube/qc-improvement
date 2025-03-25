from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from browser_use import ActionResult, Agent, Controller,  BrowserConfig, Browser, AgentHistoryList
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from pydantic import SecretStr
import base64
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")
# Initialize the model
llm = llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

controller = Controller()
browser = None
context = None


#Function to save a base 64  to a file
@controller.action("Save image buffer to file")
async def save_img(filename: str ="screenshot.png", output_folder: str = "screenshots"):
    global context
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Save the screenshot to the specified file
        base64 = await context.take_screenshot(full_page=False)
        file_path = save_screenshot_from_base64(base64, filename, output_folder)
        return f"Screenshot saved: {file_path}"
    finally:
        context.close()

def save_screenshot_from_base64(screenshot_b64: str, filename = "screenshot.png", output_folder = "screenshots") -> str:
    os.makedirs(output_folder, exist_ok=True)
    
    # Decode the base64 string
    screenshot_data = base64.b64decode(screenshot_b64)
    # Create the full file path
    file_path = os.path.join(output_folder, filename)
    # Save the screenshot to a file
    with open(file_path, "wb") as f:
        f.write(screenshot_data)
    return file_path

from playwright.sync_api import sync_playwright

@controller.action("Capture screenshot")
def hover_and_screenshot(url: str, selector: str, screenshot_name: str = "hover_menu.png"):
    """Opens a webpage, hovers over an element, waits 7 seconds, and takes a screenshot."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser
        page = browser.new_page(viewport={"width": 1920, "height": 1020})  # Set window size

        page.goto(url)  # Navigate to the target website

        # Hover over the specified element
        page.hover(selector)

        page.wait_for_timeout(7000)  # Wait for 7 seconds

        full_path = os.path.join("screenshots", screenshot_name)

        # Take a screenshot after hovering
        page.screenshot(path=full_path)

        print(f"Screenshot saved as {screenshot_name} after hovering!")

        browser.close()

# Function to apppend data like a log
@controller.action("Append information to log")
def append_log(log: str):
    with open('log.txt', 'a') as f:
        f.write(log + '\n')
    return "Log appended"


taks_main = """
Important Considerations:
✅ Ensure elements are fully loaded before interacting.
✅ Maintain the hover state for a few seconds before proceeding.
✅ Avoid clicking while hovering.
✅ Do not extract all the text from the page; only extract the required text to save token
open the stock info URL: https://company.lottechilsung.co.kr/kor/invest/stockinfo/list.do
Steps:
Extract the following data:
현재가격 (Current Price): Extract only the numeric value (remove text and hidden elements).
전일대비 (Change from Previous Day): Extract only the numeric value (remove text and hidden elements).
2️⃣
open the main page URL: https://company.lottechilsung.co.kr/kor/main/index.do
Steps:
Extract the stock price displayed under:
롯데칠성음료 보통주 (Lotte Chilsung Beverage Common Stock).
Extract text 하락" (Decline).

3️⃣ Compare and Log the Results
Get the current date and time as a string.
Append an empty line to the log file:

append_log("\n")
Log the start time:

append_log("Start log: " + str(current_date_time))
📌 Compare "현재가격" (Current Price)
If they match:

append_log("Match! 현재가격 (Current Price) matches 롯데칠성음료 보통주 (Lotte Chilsung Beverage Common Stock): " + str(current_price))
If they don’t match:

append_log("Mismatch! 현재가격 (Current Price) from Stock Info Page: " + str(current_price) +  
           " vs 롯데칠성음료 보통주 (Lotte Chilsung Beverage Common Stock) from Main Page: " + str(main_page_price))
📌 Compare "전일대비" (Change from Previous Day)
If they match:

append_log("Match! 전일대비 (Change from Previous Day) matches hiddenTxt 하락 (Decline): " + str(change_from_previous_day))
If they don’t match:

append_log("Mismatch! 전일대비 (Change from Previous Day) from Stock Info Page: " + str(change_from_previous_day) +  
           " vs hiddenTxt 하락 (Decline) from Main Page: " + str(main_page_change))
"""

task_test = "Go to https://github.com/, scroll down by one page and take screenshot the page using save_img function. Save the screenshot as 'github_screenshot.png'." 

task_coomate = """

Task: Navigate to a webpage, hover over a specific element, and capture a screenshot.
Steps:
Open the webpage: Navigate to https://www.coolmate.me/.
Find and hover: Locate a clickable element containing the text "CARE & SHARE" and hover over it without clicking.
Capture the screenshot: Use the save_img function to take a screenshot and save it as "coolmate_screenshot.png".
End the script after capturing the screenshot.

"""

async def main():
    # Create agent with the model

    config = BrowserContextConfig(
        browser_window_size={'width': 1920, 'height': 1020},
    )

    config_browser = BrowserConfig(
        headless=False,
        disable_security=True,
    )

    global browser
    global context
    browser = Browser(config=config_browser)
    context = BrowserContext(browser=browser, config=config)
    agent = Agent(
        browser_context=context,
        task=taks_main,
        llm=llm,
        controller=controller,
        save_conversation_path="./logs/log",
    )
    result: AgentHistoryList = await agent.run()
    print(result.urls())
    # close the browser context

    if (result.is_done()): 
        status = "Success" if result.is_successful() else "Failed"
        append_log(f"Agent finished with result: {status},used {result.total_input_tokens()} input tokens in {result.total_duration_seconds()} seconds")
        await context.close()

asyncio.run(main())