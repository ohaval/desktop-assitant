import tkinter as tk
import re
import ipaddress

import clipboard


class Assitant:
    IP_REGEX = r"(?:\d{1,3}\.){3}\d{1,3}"
    MAC_REGEX = r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"
    NORMAL_REQUEST_HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like\
                                             Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    HTTP_OK = 200
    ERRORS_ALIVE_TIME = 15000

    def __init__(self):
        self.root = None
        self.canvas = None
        self.main_frame = None
        self.error_frame = None

        self.tb_input = None

        self.load_layout()

    def load_layout(self):
        # Basic GUI layout
        self.root = tk.Tk()
        self.root.title("Desktop Assitant")

        self.canvas = tk.Canvas(self.root, width=600, height=1000, bg="#b3ffff")
        self.canvas.pack()

        # Main results frame
        self.main_frame = tk.Frame(self.root, bg="#00cccc")
        self.main_frame.place(relwidth=0.65, relheight=0.8, relx=0, rely=0)

        # Errors frame
        self.error_frame = tk.Frame(self.root, bg="black")
        self.error_frame.place(relwidth=0.3, relheight=0.8, relx=0.7, rely=0)

        # input text box
        self.tb_input = tk.Entry(self.root, width=30)
        self.tb_input.place(x=10, y=1060)

        self.root.geometry("+1300+0")

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
            return False  # TODO

        if not len(matches):
            self.show_error(f"0 {key}s found in input")

        return matches

    def show_error(self, error_message):
        label = tk.Label(self.error_frame, text=error_message, bg="black", fg="red")
        label.pack()
        label.after(Assitant.ERRORS_ALIVE_TIME, label.destroy)
