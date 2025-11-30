# TODO handle sudo commands. Currently they just ask for a passwoed in the shell this script is running in
# TODO improve error handling
import re
import os
import subprocess
import time

from playwright.sync_api import sync_playwright



def add_to_doc(locator, text, newline):
    locator.click()
    if(newline):
        locator.type(f"\n{text}\n")
    else:
        locator.type(f"\n{text}")


def clear(locator):
    locator.press('Control+A')
    locator.press('Backspace')


def run():
    with sync_playwright() as p:
        #starts playwright and goes to the word document
        context = p.chromium.launch(headless=True).new_context(
            storage_state="auth.json"
        )
        page = context.new_page()
        page.goto("#INSERT YOUR DOCUMENT LINK HERE")
        frame_selector = "#WacFrame_Word_0"#i frame that contains the text of the word document
        frame_locator = page.frame_locator(frame_selector) 
        locator = frame_locator.locator("#WACViewPanel_EditingElement")# actual div containing text

        time.sleep(5)
        clear(locator)#clear the document on script start

        hostname = os.uname()[1]
        user = os.getlogin()
        dir = f"/home/{user}" # start at the user's home directory not the location this script is ran
        char_limit = 5000 #defualt character limit of commands and outputs

        while(True):#main loop
            time.sleep(1)

            text = locator.inner_text().strip()
            prompt = f"{user}@{hostname}:{dir}$ "

            if(text == ""):#prints the command prompt
                add_to_doc(locator, prompt, False)
                
            if(text.endswith(";;")):# put ;; at the end of a line to execute it
                command = text[len(prompt):-2]
                print("command is:" +command )

                try:#catch the user inputing commands that crash
                    output = ""

                    if(len(output)>char_limit or len(command)>char_limit and char_limit!=-1):#makes sure the char limit is not exceeded
                        output = f"output is greater then the character limit of {char_limit}. Run 'char_limit -1' to remove this restriction.\n"

                    elif(command.startswith("cd")):# specific case for handling the cd command. This keeps the current working directory persistant
                        ndir = command[2:].strip()
                        if (ndir == ""):# handles an empty cd command (cd to home dir)
                            dir = f"/home/{user}"
                        elif(ndir.startswith("/") and os.path.exists(ndir)):
                            dir = ndir
                            print("abs path: "+dir)
                        elif(ndir == ".."):#handle going to the parent directory
                            pardir = os.path.dirname(dir)
                            print("pardir is : "+ pardir)
                            if(os.path.exists(pardir)):
                                dir = pardir
                        elif(os.path.exists(os.path.join(dir, ndir))):
                            dir = os.path.join(dir,ndir)
                            print("nonabsdir: " +dir)
                        else:
                            raise Exception(f"{dir}{ndir} could not be resolved to a valid path")

                    elif(command == "^l"):#command to clear the doc
                        clear(locator)
                    elif(command.startswith("char_limit")):#command for changing the character limit. (-1 means no char limit)
                        char_limit = command.split()[1]
                        output = f"max length of input/output changed to {char_limit}"

                    else:
                        output = subprocess.check_output(command, cwd=dir, shell=True)
                        output = output.decode('utf-8', errors = 'replace')

                    add_to_doc(locator, output, True)

                except Exception as e:
                    print(f"the command {command} threw an error")
                    add_to_doc(locator, f"ERROR: {e}", True)

run()#runs main function
