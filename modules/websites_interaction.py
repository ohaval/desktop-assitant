import requests
import tkinter as tk


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