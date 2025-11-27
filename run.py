import re
import subprocess
import time
from playwright.sync_api import sync_playwright

def add_to_doc(locator, text):
                    locator.click()
                    locator.type(f"\n{text}\n")
def run():
    with sync_playwright() as p:
        context = p.chromium.launch(headless=False).new_context(
            storage_state="auth.json"
        )
        page = context.new_page()

        page.goto(#INSERT YOUR DOCUMENT LINK HERE)
        frame_selector = "#WacFrame_Word_0"
        frame_locator = page.frame_locator(frame_selector) 
        locator = frame_locator.locator("#WACViewPanel_EditingElement")
        while(True):
            time.sleep(1)
            text = locator.inner_text().strip()
            # if(text ==""):
                #print the user and the directory as one might see on a terminal. Figure out some way to make ssh work and keeping working directory persistant
            if(re.match(r'\$\$(.*?)\$\$', text)):
                command = text[2:-2]
                print("command is:" +command )
                try:
                    output = subprocess.check_output(command, shell=True)
                    output = output.decode('utf-8', errors = 'replace')
                    print(f"command output is: {output}")
                    add_to_doc(locator, output)
                except Exception as e:
                    print(f"the command{command}threw an error")
                    print(e)
                    add_to_doc(locator, f"ERROR: {e}")
run()
