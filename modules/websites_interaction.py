import json
import tkinter as tk
import sys; sys.path.append("..")

import requests
from bs4 import BeautifulSoup

from assitant import Assitant
from modules.websites_interaction_files.IP import IP


class WebsiteInteraction(Assitant):
    IP_URL = "https://iplocation.com/"
    MAC_URL = "https://macvendors.com/query/{mac}"
    GOOGLE_URL = "https://www.google.com/search?q={term}"
    GOOGLE_MAX_RESULTS = 3

    def start(self):
        btn = tk.Button(self.root, text="Check MAC Address", padx=50, pady=10, command=self.mac_search)
        btn.pack()

        btn = tk.Button(self.root, text="Check IP", padx=50, pady=10, command=self.ip_search)
        btn.pack()

        btn = tk.Button(self.root, text="Google", padx=50, pady=10, command=self.google_search)
        btn.pack()

        self.root.mainloop()

    def mac_search(self):
        mac_addresses = self.extract_values(self.get_values(), key="mac")

        if mac_addresses:
            text = ""
            for mac in mac_addresses:
                if text:
                    text += "\n"

                page = requests.get(WebsiteInteraction.MAC_URL.format(mac=mac), headers=Assitant.NORMAL_REQUEST_HEADERS)
                if page.status_code != Assitant.HTTP_OK:
                    self.show_error(f"Response error ({page.status_code})")
                    continue

                vendor = page.text
                text += f"{mac}\n{vendor}\n"

            text_obj = tk.Text(self.main_frame, height=text.count("\n"), width=200, bg="#00ccce")
            text_obj.insert(tk.INSERT, text)
            text_obj.pack()

    def ip_search(self):
        ip_addresses = self.extract_values(self.get_values(), key="ip")

        if ip_addresses:
            text = ""
            for ip in ip_addresses:
                if text:
                    text += "\n"

                payload = {"ip": ip}
                page = requests.post(WebsiteInteraction.IP_URL, headers=Assitant.NORMAL_REQUEST_HEADERS, data=payload)
                if page.status_code != Assitant.HTTP_OK:
                    self.show_error(f"Response error ({page.status_code})")
                    continue

                try:
                    response_data = json.loads(page.text)
                except json.decoder.JSONDecodeError:
                    self.show_error(f"Information recieved for ip '{ip}'\n is in bad format.\n({page.text})")
                    continue

                ip = IP(response_data)
                text += ip.summary()

            text_obj = tk.Text(self.main_frame, height=text.count("\n"), width=200, bg="#00cccc")
            text_obj.insert(tk.INSERT, text)
            text_obj.pack()

    def google_search(self):
        term = self.get_values()

        page = requests.get(WebsiteInteraction.GOOGLE_URL.format(term=term), headers=Assitant.NORMAL_REQUEST_HEADERS)
        if page.status_code != Assitant.HTTP_OK:
            self.show_error(f"Response error ({page.status_code})")
            return

        soup = BeautifulSoup(page.content, 'lxml')
        results = soup.find_all('div', class_='r')[:WebsiteInteraction.GOOGLE_MAX_RESULTS]

        text = ""
        additional_nl = 0
        for result in results:
            if text:
                text += "\n"

            title = result.find('h3', class_="LC20lb DKV0Md").text
            if len(title) > 48:
                additional_nl += 1

            text += f"{title}\n"

            href = result.find('a').get('href')
            if len(href) > 48:
                href = href[:45] + "..."
            text += f"{href}\n"

        text_obj = tk.Text(self.main_frame, height=text.count("\n") + additional_nl, width=200, bg="#00ccca")
        text_obj.insert(tk.INSERT, text)
        text_obj.pack()


def main():
    obj = WebsiteInteraction()
    obj.start()


if __name__ == "__main__":
    main()
