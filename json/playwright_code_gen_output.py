import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, email, password) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.lottemart.vn/login")
    page.get_by_role("textbox", name="Email/Số điện thoại *").click()
    page.get_by_role("textbox", name="Email/Số điện thoại *").fill(email)
    page.get_by_role("textbox", name="Mật khẩu *").click()
    page.get_by_role("textbox", name="Mật khẩu *").fill(password)
    page.get_by_role("button", name="Đăng nhập").click()

    # ---------------------
    # Wait for navigation to complete - more reliable than fixed assertions
    try:
        # Option 1: Wait for URL to change from login page
        page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
        print(f"Successfully logged in! Current URL: {page.url}")
        
        # Option 2: Look for elements that indicate successful login
        if page.get_by_text("Đăng xuất").is_visible(timeout=5000) or page.get_by_text("Tài khoản của tôi").is_visible(timeout=5000):
            print("Verified login success - found account elements")
            
        # You can validate more aspects of successful login here
        
    except Exception as e:
        print(f"Login might have failed: {str(e)}")
        # Take screenshot on failure
        page.screenshot(path="../screenshots/login_failure.png")
        
        # Check for error messages
        error_text = page.text_content("body")
        print(f"Page content: {error_text[:200]}...")  # Print first 200 chars
        
        # Re-raise to fail the test
        raise

    # Keep browser open for debugging
    input("Press Enter to close the browser...")
    
    # ---------------------
    context.close()
    browser.close()



with sync_playwright() as playwright:
    email = input("Enter email: ")
    password = input("Enter password: ")
    run(playwright, email, password)