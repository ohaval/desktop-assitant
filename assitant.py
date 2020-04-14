import tkinter as tk
import clipboard as cp
import requests
import json
from IP import IP
import re
import ipaddress
from bs4 import BeautifulSoup


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


def ip_search(ip_addresses=None):
    if not ip_addresses:
        ip_addresses = get_values_from_clip(key="ip")

    if ip_addresses:
        summary = ""
        for ip in ip_addresses:
            if summary:
                summary += "\n"

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
            summary += ip.summary()

        text_obj = tk.Text(main_frame, height=summary.count("\n"), width=TEXT_WIDTH, bg="#00cccc")
        text_obj.insert(tk.INSERT, summary)
        text_obj.pack()


def google_search(results_count=3):
    text_box_value = tb_input.get()
    if text_box_value:
        term = text_box_value
    else:
        term = cp.paste()

    page = requests.get(GOOGLE_URL.format(term=term), headers=headers)
    if page.status_code != 200:
        show_error(f"Response error ({page.status_code})")
        return

    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find_all('div', class_='r')[:3]

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


# Example layout
root = tk.Tk()
root.title("Desktop Assitant")

canvas = tk.Canvas(root, height=1000, width=600, bg="#b3ffff")
canvas.pack()

# Main results frame
main_frame = tk.Frame(root, bg="#00cccc")
main_frame.place(relwidth=0.65, relheight=0.8, relx=0, rely=0)

# Errors frame
error_frame = tk.Frame(root, bg="black")
error_frame.place(relwidth=0.3, relheight=0.8, relx=0.7, rely=0)

# Buttons
check_mac = tk.Button(root, text="Check MAC Address", padx=50, pady=10, command=mac_search)
check_mac.pack()

check_ip = tk.Button(root, text="Check IP", padx=50, pady=10, command=ip_search)
check_ip.pack()

check_ip = tk.Button(root, text="Google", padx=50, pady=10, command=google_search)
check_ip.pack()

tb_input = tk.Entry(root, width=30, )
tb_input.place(x=10, y=1060)

root.geometry("+1300+0")

root.mainloop()

