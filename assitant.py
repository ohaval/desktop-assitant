import tkinter as tk
import clipboard as cp
import requests
from bs4 import BeautifulSoup
import json
from IP import IP
import re


MAC_URL = "https://macvendors.com/query/{mac}"
IP_URL = "https://iplocation.com/"
MAC_REGEX = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"


def mac_to_vendor(mac_address=None):
    mac_address = cp.paste()
    if re.match(MAC_REGEX, mac_address):
        text = requests.get(MAC_URL.format(mac=mac_address)).text
    else:
        text = f"Not a mac address: {mac_address}"

    label = tk.Label(frame, text=text, bg="green")
    label.pack()

    return text


def ip_info(ip_address=None):
    ip_address = cp.paste()

    payload = {"ip": ip_address}
    page = requests.post(IP_URL, data=payload)
    response_data = json.loads(page.text)

    ip = IP(response_data)
    text = ""

    for k, v in ip.minimal_info().items():
        text += f"{k.ljust(25)}:{v}\n"
    print(text)

    label = tk.Label(frame, text=text, bg="yellow")
    label.pack()


root = tk.Tk()

canvas = tk.Canvas(root, height=600, width=600, bg="#c6c6ec")
canvas.pack()

frame = tk.Frame(root, bg="#8c8cd9")
frame.place(relwidth=0.9, relheight=0.6, relx=0.2, rely=0.04)

# Buttons
check_mac = tk.Button(root, text="CheckAddress", padx=20, pady=10, command=mac_to_vendor)
check_mac.pack()

check_ip = tk.Button(root, text="CheckIP", padx=20, pady=10, command=ip_info)
check_ip.pack()

root.mainloop()













