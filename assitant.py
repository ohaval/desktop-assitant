import tkinter as tk
import clipboard as cp
import requests
import json
from IP import IP
import re
import ipaddress
from bs4 import BeautifulSoup
import os
import importlib
from functools import partial


MAC_URL = "https://macvendors.com/query/{mac}"
MAC_REGEX = "(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"
IP_URL = "https://iplocation.com/"
IP_REGEX = "(?:\d{1,3}\.){3}\d{1,3}"
GOOGLE_URL = "https://www.google.com/search?q={term}"
ERRORS_ALIVE_TIME = 15000
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163\
 Safari/537.36"

TEXT_WIDTH = 200

headers = {'User-Agent': USER_AGENT}

method_pointer = ""


def show_error(text):
    label = tk.Label(error_frame, text=text, bg="black", fg="red")
    label.pack()
    label.after(ERRORS_ALIVE_TIME, label.destroy)


def extract_values(data, key):
    """Possible keys are: ip, mac"""

    if key == "ip":
        matches = re.findall(IP_REGEX, data)
        matches = set(filter(lambda ip: False if ipaddress.ip_address(ip).is_private else True, matches))

    elif key == "mac":
        matches = set(re.findall(MAC_REGEX, data))

    else:
        # For now
        return False

    if not len(matches):
        show_error(f"0 {key}s found in input")

    return matches


def mac_search(input_):
    mac_addresses = extract_values(input_[0], "mac")

    if mac_addresses:
        text = ""
        for mac in mac_addresses:
            if text:
                text += "\n"

            page = requests.get(MAC_URL.format(mac=mac))
            if page.status_code != 200:
                show_error(f"Response error ({page.status_code})")
                continue

            vendor = page.text
            text += f"{mac}:\n{vendor}\n"

        text_obj = tk.Text(main_frame, height=text.count("\n"), width=TEXT_WIDTH, bg="#00cccc")
        text_obj.insert(tk.INSERT, text)
        text_obj.pack()


def ip_search(input_):
    ip_addresses = extract_values(input_[0], "ip")

    if ip_addresses:
        text = ""
        for ip in ip_addresses:
            if text:
                text += "\n"

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
            text += ip.summary()

        text_obj = tk.Text(main_frame, height=text.count("\n"), width=TEXT_WIDTH, bg="#00cccc")
        text_obj.insert(tk.INSERT, text)
        text_obj.pack()


def google_search(input_, results_count=3):
    term = input_[0]

    page = requests.get(GOOGLE_URL.format(term=term), headers=headers)
    if page.status_code != 200:
        show_error(f"Response error ({page.status_code})")
        return

    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find_all('div', class_='r')[:results_count]

    text = ""
    additional_nl = 0
    for result in results:
        if text:
            text += "\n"
        title = result.find('span', dir='ltr').text
        if len(title) > 48:
            additional_nl += 1
        text += f"{title}\n"
        href = result.find('a').get('href')
        if len(href) > 48:
            href = href[:45] + "..."
        text += f"{href}\n"

    text_obj = tk.Text(main_frame, height=text.count("\n") + additional_nl, width=TEXT_WIDTH, bg="#00cccc")
    text_obj.insert(tk.INSERT, text)
    text_obj.pack()


def call_manage(func):
    """Input methods for function are: Text box, clipboard. (at the moment)"""
    text_box_value = tb_input.get()
    if text_box_value:
       func((text_box_value, 'tb'))

    else:
        data = cp.paste()
        func((data, 'clipboard'))


# Example layout
root = tk.Tk()
root.title("Desktop Assitant")

canvas = tk.Canvas(root, width=600, height=1000, bg="#b3ffff")
canvas.pack()

# Main results frame
main_frame = tk.Frame(root, bg="#00cccc")
main_frame.place(relwidth=0.65, relheight=0.8, relx=0, rely=0)

# Errors frame
error_frame = tk.Frame(root, bg="black")
error_frame.place(relwidth=0.3, relheight=0.8, relx=0.7, rely=0)



# load modules

files = []
for file in os.listdir("modules"):
    if not file.startswith("__"):
        file = file[:-3]
        globals()[file] = importlib.import_module(f"modules.{file}")
        files.append((file, globals()[file]))

print(files)

functions = []
for file in files:
    methods = [func for func in dir(file[1]) if not func.startswith("__")]
    for method in methods:
        method_full_name = file[0] + "." + method
        exec(f"method_pointer = {method_full_name}")
        if method not in functions and callable(method_pointer):
            functions.append((method_full_name, method_pointer))
print(functions)


for function in functions:
    btn = tk.Button(root, text=function[0], padx=50, pady=10, command=partial(call_manage, function[1]))
    btn.pack()


# Buttons
# check_mac = tk.Button(root, text="Check MAC Address", padx=50, pady=10, command=partial(call_manage, 'mac_search'))
# check_mac.pack()
#
# check_ip = tk.Button(root, text="Check IP", padx=50, pady=10, command=partial(call_manage, 'ip_search'))
# check_ip.pack()
#
# google = tk.Button(root, text="Google", padx=50, pady=10, command=partial(call_manage, 'google_search'))
# google.pack()

# input text box
tb_input = tk.Entry(root, width=30)
tb_input.place(x=10, y=1060)

root.geometry("+1300+0")
root.mainloop()
