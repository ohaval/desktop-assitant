import tkinter as tk
import json

import requests
from bs4 import BeautifulSoup

import _set_path
from assitant import Assitant
from basic_reconnaissance_files.IP import IP


class BasicReconnaissance(Assitant):
    IP_URL = "https://iplocation.com/"
    MAC_URL = "https://macvendors.com/query/{mac}"
    GOOGLE_URL = "https://www.google.com/search?q={term}"
    GOOGLE_MAX_RESULTS = 3

    def __init__(self):
        Assitant.__init__(self)
        self.TEXT_OBJECTS = []
        self.check_box_value = tk.IntVar()

    def start(self):
        self.add_button("Clean", self.clean_text)
        self.add_button("Check MAC Address", self.mac_search)
        self.add_button("Check IP", self.ip_search)
        self.add_button("Google", self.google_search)
        self.add_button("Run All!", self.run_everything)

        tk.Checkbutton(self.root, text="FullInfo", variable=self.check_box_value).place(relx=0.35, rely=0.805)

        self.root.mainloop()

    def clean_text(self):
        for text_obj in self.TEXT_OBJECTS:
            text_obj.destroy()
        self.TEXT_OBJECTS = []

    def run_everything(self):
        self.mac_search()
        self.ip_search()
        self.google_search()

    def mac_search(self):
        mac_addresses = self.extract_values(self.get_values(), key="mac")

        if mac_addresses:
            text = ""
            for mac in mac_addresses:
                if text:
                    text += "\n"

                page = requests.get(self.MAC_URL.format(mac=mac), headers=Assitant.NORMAL_REQUEST_HEADERS)
                if page.status_code != Assitant.HTTP_OK:
                    self.show_error(f"Response error ({page.status_code})")
                    continue

                vendor = page.text
                text += f"{mac}\n{vendor}\n"

            self.TEXT_OBJECTS.append(self.add_text_to_main_frame(text, text.count("\n")))

    def ip_search(self):
        ip_addresses = self.extract_values(self.get_values(), key="ip")

        if ip_addresses:
            text = ""
            for ip in ip_addresses:
                if text:
                    text += "\n"

                payload = {"ip": ip}
                page = requests.post(self.IP_URL, headers=Assitant.NORMAL_REQUEST_HEADERS, data=payload)
                if page.status_code != Assitant.HTTP_OK:
                    self.show_error(f"Response error ({page.status_code})")
                    continue

                try:
                    response_data = json.loads(page.text)
                except json.decoder.JSONDecodeError:
                    self.show_error(f"Information recieved for ip '{ip}'\n is in bad format.\n({page.text})")
                    continue

                ip = IP(response_data)
                text += ip.summary(level=self.check_box_value.get())

            self.TEXT_OBJECTS.append(self.add_text_to_main_frame(text, text.count("\n")))

    def google_search(self):
        max_title_length = 46

        term = self.get_values()

        page = requests.get(self.GOOGLE_URL.format(term=term), headers=Assitant.NORMAL_REQUEST_HEADERS)
        if page.status_code != Assitant.HTTP_OK:
            self.show_error(f"Response error ({page.status_code})")
            return

        soup = BeautifulSoup(page.content, 'lxml')
        results = soup.find_all('div', class_='r')[:self.GOOGLE_MAX_RESULTS]

        text = ""
        additional_nl = 0
        for result in results:
            if text:
                text += "\n"

            title = result.find('h3', class_="LC20lb DKV0Md").text
            if len(title) > max_title_length:
                additional_nl += 1

            text += f"{title}\n"

            href = result.find('a').get('href')
            if len(href) > max_title_length:
                href = href[:max_title_length - 3] + "..."
            text += f"{href}\n"

        self.TEXT_OBJECTS.append(self.add_text_to_main_frame(text, text.count("\n") + additional_nl))


def main():
    obj = BasicReconnaissance()
    obj.start()


if __name__ == "__main__":
    main()
