from playwright.sync_api import sync_playwright, Page 

def run_browser_session():
    with sync_playwright() as p:
        browser = p.chrome.launch(headless=False)
        
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(#INSERT YOUR DOCUMENT LINK HERE)
        input("Press Enter AFTER you have successfully logged in")
        context.storage_state(path="auth.json")
        cookies = context.cookies()        
        
        
run_browser_session()
