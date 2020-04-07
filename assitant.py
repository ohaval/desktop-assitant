import tkinter as tk
import clipboard as cp
import requests
import json
from IP import IP
import re
import ipaddress
import time
from bs4 import BeautifulSoup


MAC_URL = "https://macvendors.com/query/{mac}"
MAC_REGEX = "(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"
IP_URL = "https://iplocation.com/"
IP_REGEX = "(?:\d{1,3}\.){3}\d{1,3}"
ERRORS_ALIVE_TIME = 15000

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/80.0.3987.163 Safari/537.36'}


def show_error(text):
    label = tk.Label(error_frame, text=text, bg="black", fg="red")
    label.pack()
    label.after(ERRORS_ALIVE_TIME, label.destroy)


def get_values_from_clip(key):
    clip_content = cp.paste()

    if key == "ip":
        matches = re.findall(IP_REGEX, clip_content)
        matches = set(filter(lambda ip: False if ipaddress.ip_address(ip).is_private else True, matches))

    elif key == "mac":
        matches = set(re.findall(MAC_REGEX, clip_content))

    else:
        # For now
        return False

    if not len(matches):
        show_error(f"0 {key}s found in input")

    return matches


def mac_search(mac_addresses=None):
    if not mac_addresses:
        mac_addresses = get_values_from_clip(key="mac")

    if mac_addresses:
        for mac in mac_addresses:
            page = requests.get(MAC_URL.format(mac=mac))
            if page.status_code != 200:
                show_error(f"Response error ({page.status_code})")
                continue

            vendor = page.text
            text = f"{mac}:\n{vendor}"
            label = tk.Label(main_frame, text=text, bg="#00cccc", font=('Arial', 16))
            label.pack()


def ip_search(ip_addresses=None):
    if not ip_addresses:
        ip_addresses = get_values_from_clip(key="ip")

    if ip_addresses:
        for ip in ip_addresses:
            payload = {"ip": ip}
            page = requests.post(IP_URL, headers=headers, data=payload)
            if page.status_code != 200:
                show_error(f"Response error ({page.status_code})")
                continue

            try:
                response_data = json.loads(page.text)
            except json.decoder.JSONDecodeError:
                show_error(f"Information recieved for ip '{ip}'\n is in bad format.\n({page.text})")
                continue

            ip = IP(response_data)
            summary = ip.summary()
            label = tk.Label(main_frame, text=summary, bg="#00cccc")
            label.pack()


# Example layout
root = tk.Tk()

canvas = tk.Canvas(root, height=1000, width=600, bg="#b3ffff")
canvas.pack()

# Main results frame
main_frame = tk.Frame(root, bg="#00cccc")
main_frame.place(relwidth=0.45, relheight=0.8, relx=0, rely=0)

# Errors frame
error_frame = tk.Frame(root, bg="black")
error_frame.place(relwidth=0.45, relheight=0.8, relx=0.55, rely=0)

# Buttons
check_mac = tk.Button(root, text="Check MAC Address", padx=50, pady=10, command=mac_search)
check_mac.pack()

check_ip = tk.Button(root, text="Check IP", padx=50, pady=10, command=ip_search)
check_ip.pack()

root.geometry("+1300+0")

root.mainloop()
