# Automation.py
import asyncio
import keyboard
import os
import subprocess
import requests
import webbrowser
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
from typing import List
# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# CSS classes for HTML parsing
classes = ["zCubwf", "HgKELc", "LTKOO sY7ric", "Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee", 
            "COMPL", "DRAKE6", "ITK00 S7T4G", "XCLOP", "JSIT Wk_Dk FxW5b YwPhnf", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO",
           "vlzY6d", "webanswers.webanswers-webanswers_table__webanswers-table", "dDoNo ikb4b gsrt",
           "sxLaOe", "VQF4g", "qv3Wpe","kuo-rdesc", "SPZz6b"]

# User agent for web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4096.75 Safari/537.36'

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Professional responses and chat setup
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}. You're a content writer contant like letters,codes,applications,essays,notes,song,poems etc."}]

# Search functions
def GoogleSearch(query):
    search(query)
    return True

def Content(topic):

    def OpenNotepad(file):
        default_text_editor= "notepad.exe"
        subprocess.Popen(['notepad.exe', file])

    # topic = topic.replace("Content ", "")
    # content = ContentWriterAI(topic) 

# Content generation functions
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer


    topic: str =topic.replace("Content", "")
    ContentByAI=ContentWriterAI(topic)

    filename = rf"Data\{topic.lower().replace(' ', '')}.txt"
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    OpenNotepad(filename)
    return True
# Content("write a c program to copu a string which is inputedby the user to a sub string ")


def YouTubeSearch(topic):
    url4Search = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

# PlayYoutube("DSA is FUN (You've Just Been Learning It Wrong)")

# App control functions
def OpenApp(app, sess=requests.Session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup=BeautifulSoup(html,"html.parser")
            links=soup.find_all('a',{"jsname":"UWckNb"})
            return [link.get("href") for link in links]
    
        def search_google(query):

            url=f"https://www.google.com/search?q={query}"
            headers={"User-Agent":useragent}
            response=sess.get(url,headers=headers)

            if(response.status_code==200):
                return response.text
            else:
                print("Failed to retrieve search result.")
                return None
            


        html = search_google(app) 
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
                return True
        return False

def CloseApp(app):
    if "chrome" in app.lower():
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# System control functions
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    
    def unmute():
        keyboard.press_and_release("volume mute")
    
    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")
    
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    else:
        print(f"Unknown system command: {command}")
        return False
    
    return True


# Main automation functions
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    
    for command in commands:
        if(command.startswith("open ")):
            if("open it" in command):
                pass
            if("Open file"==command):
                pass
            else:
                fun=asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))
        
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))
        
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))
        
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))
        
        elif command in ["mute", "unmute", "volume up", "volume down"]:
            funcs.append(asyncio.to_thread(System, command))
        
        elif command.startswith("general "):
            pass  # Placeholder from screenshot 309
        
        elif command.startswith("realtime "):
            pass  # Placeholder from screenshot 309
        
        else:
            print(f"No Function Found For: {command}")  # From screenshot 313
    
    results = await asyncio.gather(*funcs, return_exceptions=True)
    
    for result in results:  # From screenshot 313
        if isinstance(result, str):
            yield result
        else:
            yield str(result)

async def Automation(commands: list[str]):

        async for result in TranslateAndExecute(commands):
            pass

        return True

if __name__=="__main__":
    asyncio.run(Automation([]))