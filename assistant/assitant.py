import tkinter as tk
import re
import ipaddress

import clipboard


class Assitant:
    WINDOW_WIDTH = 576
    TITLE = "Desktop Assitant"
    IP_REGEX = r"(?:\d{1,3}\.){3}\d{1,3}"
    MAC_REGEX = r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"
    NORMAL_REQUEST_HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like\
                                             Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    HTTP_OK = 200
    ERRORS_ALIVE_TIME = 15000

    def __init__(self):
        self.screen_size = None

        self.root = None
        self.main_frame = None
        self.error_frame = None
        self.tb_input = None
        self.buttons = 0

        self.load_layout()

    def load_layout(self):
        # Basic GUI layout
        self.root = tk.Tk()
        self.screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())

        self.root.title(self.TITLE)
        self.root.configure(width=self.WINDOW_WIDTH, height=int(self.screen_size[1]), bg='skyblue')

        # Main results frame
        self.main_frame = tk.Frame(self.root, bg="#00cccc")
        self.main_frame.place(relwidth=0.65, relheight=0.8, relx=0, rely=0)

        # Errors frame
        self.error_frame = tk.Frame(self.root, bg="black")
        self.error_frame.place(relwidth=0.3, relheight=0.8, relx=0.7, rely=0)

        # input text box
        self.tb_input = tk.Entry(self.root, width=int(self.WINDOW_WIDTH * 0.048))
        self.tb_input.place(relx=0.35, rely=0.83)

        self.root.geometry(f"+{self.screen_size[0] - self.WINDOW_WIDTH}+0")

        # self.mainloop() -> This should be done inside the module object in the start function.

    def get_values(self):
        """Return data for processing based on order.
           1) Text box
           2) Clipboard
        """
        text_box_value = self.tb_input.get()
        if text_box_value:
            return text_box_value

        clipboard_value = clipboard.paste()
        if clipboard_value:
            return clipboard_value

        return False

    def extract_values(self, data, key, regex=None):
        """Possible keys are: ip, mac or to provide a regex expression."""

        if regex:
            matches = re.findall(regex, data)

        elif key == "ip":
            matches = re.findall(Assitant.IP_REGEX, data)
            matches = set(ip for ip in matches if not ipaddress.ip_address(ip).is_private)

        elif key == "mac":
            matches = set(re.findall(Assitant.MAC_REGEX, data))

        else:
            self.show_error(f"extract_values function was called with unknown key value - {key}")
            return False

        if not len(matches):
            self.show_error(f"0 {key}s found in input")

        return matches

    def show_error(self, error_message):
        label = tk.Label(self.error_frame, text=error_message, bg="black", fg="red")
        label.pack()
        label.after(Assitant.ERRORS_ALIVE_TIME, label.destroy)

    def add_button(self, text, func):
        if self.screen_size[1] < 1140:
            pady = 0.035
        else:
            pady = 0.03

        self.buttons += 1
        if self.buttons <= 5:
            relx = 0
            rely = 0.805 + ((self.buttons - 1) % 5) * pady
            width = 25
            text = text[:25]

        elif self.buttons <= 10:
            relx = 0.65
            rely = 0.805 + ((self.buttons - 1) % 5) * pady
            width = 25
            text = text[:25]

        elif self.buttons <= 13:
            relx = 0.38
            rely = 0.805 + ((self.buttons + 1) % 5) * pady
            width = 16
            text = text[:16]

        else:
            return

        btn = tk.Button(self.root, text=text, padx=5, pady=5, command=func, width=width)
        btn.place(relx=relx, rely=rely)

