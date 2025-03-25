import base64
import google.generativeai as genai
from playwright.sync_api import sync_playwright
import os
import time

# Configure the Google GenAI API key
# Replace with your actual API key
genai.configure(api_key="AIzaSyDfUtioEpZqM8cK6ClF2kSR3l0IMGYbvz8")

# Define the functions for the GenAI model to call

def open_url_and_get_html(url):
    """
    Opens a URL using Playwright and returns the HTML content.
    
    Args:
        url (str): The URL to open
        
    Returns:
        str: The HTML content of the page
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html

def find_navigation_selector(url):
    """
    Finds and returns a CSS selector for a navigation element on the page.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        str: A CSS selector targeting the navigation bar
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Common selectors for navigation elements
        nav_selectors = [
            "nav",
            "header nav",
            ".navbar",
            ".navigation",
            "#nav",
            ".nav",
            "header .menu",
            ".main-menu",
            "#navigation"
        ]
        
        # Find the first matching selector
        for selector in nav_selectors:
            if page.locator(selector).count() > 0:
                browser.close()
                return selector
                
        # If no common selectors match, try to find something that looks like navigation
        # Look for elements with multiple links that might be a navigation bar
        nav_candidates = page.eval_on_selector_all(
            "body", 
            """() => {
                const elements = Array.from(document.querySelectorAll('*'));
                return elements
                    .filter(el => el.querySelectorAll('a').length > 3)
                    .map(el => {
                        const path = [];
                        let node = el;
                        while (node) {
                            if (node.id) {
                                path.unshift('#' + node.id);
                                break;
                            } else if (node.className && typeof node.className === 'string') {
                                path.unshift('.' + node.className.split(' ')[0]);
                            } else {
                                path.unshift(node.tagName.toLowerCase());
                            }
                            node = node.parentElement;
                        }
                        return path.join(' ');
                    });
            }"""
        )
        
        browser.close()
        return nav_candidates[0] if nav_candidates else "No navigation found"

def hover_and_screenshot(url, selector):
    """
    Hovers over an element with the given CSS selector for 5 seconds and takes a screenshot.
    
    Args:
        url (str): The URL of the page
        selector (str): CSS selector of the element to hover over
        
    Returns:
        str: Base64 encoded screenshot image
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Using headless=False to ensure hover effects are visible
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(url)
        
        try:
            # Wait for the element to be visible
            page.wait_for_selector(selector, state="visible", timeout=10000)
            
            # Hover over the element
            page.hover(selector)
            
            # Wait for 5 seconds to allow hover effects to appear
            time.sleep(5)
            
            # Take a screenshot
            screenshot_bytes = page.screenshot()
            
            # Convert screenshot to base64
            base64_screenshot = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            browser.close()
            return base64_screenshot
        except Exception as e:
            browser.close()
            return f"Error taking screenshot: {str(e)}"

# Define the functions for the GenAI model to use
functions = [
    {
        "name": "open_url_and_get_html",
        "description": "Opens a URL and returns its HTML content",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to open"
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "find_navigation_selector",
        "description": "Returns a CSS selector for a navigation element on a webpage",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to analyze"
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "hover_and_screenshot",
        "description": "Hovers over an element with the given CSS selector for 5 seconds and takes a screenshot",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the page"
                },
                "selector": {
                    "type": "string",
                    "description": "CSS selector of the element to hover over"
                }
            },
            "required": ["url", "selector"]
        }
    }
]

# Example of using the GenAI model with function calling
def process_user_query(query):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    response = model.generate_content(
        query,
        generation_config={"temperature": 0.7},
        tools=[{"function_declarations": functions}]
    )
    
    # Check if the model wants to call a function
    if hasattr(response, 'candidates') and response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        function_args = function_call.args
        
        print(f"Function called: {function_name}")
        print(f"Arguments: {function_args}")
        
        # Execute the function based on name
        if function_name == "open_url_and_get_html":
            result = open_url_and_get_html(function_args["url"])
        elif function_name == "find_navigation_selector":
            result = find_navigation_selector(function_args["url"])
        elif function_name == "hover_and_screenshot":
            result = hover_and_screenshot(function_args["url"], function_args["selector"])
        else:
            result = f"Unknown function: {function_name}"
        
        # Send the function result back to the model for further processing
        follow_up_response = model.generate_content(
            [
                query,
                {"function_response": {"name": function_name, "response": {"result": result}}}
            ]
        )
        
        return follow_up_response.text
    else:
        return response.text

# Example usage
if __name__ == "__main__":
    # Example queries to test the functions
    queries = [
        "Open the website https://www.example.com and show me its HTML",
        "Find the navigation selector on https://www.python.org",
        "Go to https://www.python.org, find the navigation bar, hover over it, and take a screenshot",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        result = process_user_query(query)
        print(f"Result: {result}")
        print("-" * 50)