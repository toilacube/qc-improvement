from playwright.sync_api import sync_playwright
import os

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # Launch browser
#     page = browser.new_page(viewport={"width": 1920, "height": 1020})
    
#     page.goto("https://company.lottechilsung.co.kr/kor/main/index.do")  # Change this to your target website
    

#     # Hover over the first menu item (기업소개)
#     page.hover("ul#gnb > li.dep:nth-child(1) > a.oneD")

#     # Wait for submenu to be visible
#     page.wait_for_selector("ul.twoD", state="visible")
#     page.wait_for_timeout(7000)
#     # Take a screenshot after hovering
#     page.screenshot(path="hover_menu.png")

#     print("Screenshot taken after hovering!")
#     browser.close()

def hover_and_screenshot(url: str, selector: str, screenshot_name: str = "hover_menu.png"):
    """Opens a webpage, hovers over an element, waits 7 seconds, and takes a screenshot."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser
        page = browser.new_page(viewport={"width": 1920, "height": 1020})  # Set window size

        page.goto(url)  # Navigate to the target website

        # Hover over the specified element
        page.hover(selector)

        # Wait for submenu to be visible
        page.wait_for_selector(selector, state="visible")
        page.wait_for_timeout(7000)  # Wait for 7 seconds

        full_path = os.path.join("screenshots", screenshot_name)

        # Take a screenshot after hovering
        page.screenshot(path=full_path)

        print(f"Screenshot saved as {screenshot_name} after hovering!")

        browser.close()


def test_hover_and_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser
        page = browser.new_page(viewport={"width": 1920, "height": 1020})  # Set window size
        page.goto("https://company.lottechilsung.co.kr/kor/main/index.do#")  # Replace with the actual URL of the website

        # Selector for the "기업소개" element in the nav bar.  Adjust as needed.
        # nav_element_selector = '#gnb > li:nth-child(1) > a'
        nav_element_selector = "a[href=\"/kor/recruit/talent/contentsid/545/index.do\"]"
        # Hover over the element
        page.hover(nav_element_selector)

        # Wait for 5 seconds
        page.wait_for_timeout(5000)

        # Take a screenshot
        page.screenshot(path="hover_screenshot.png")

        browser.close()

if __name__ == "__main__":
    # Example usage
    # Navigate to the Stock Info Page
    # hover_and_screenshot("https://company.lottechilsung.co.kr/kor/invest/stockinfo/list.do", "ul#gnb > li.dep:nth-child(1) > a.oneD", "hover_menu.png")

    # Navigate to the Main Page
    test_hover_and_screenshot()
