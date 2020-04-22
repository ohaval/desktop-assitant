import tkinter as tk
import re
import ipaddress

import clipboard


class Assitant:
    WINDOW_WIDTH, WINDOW_HEIGHT = 576, 1000
    TITLE = "Desktop Assitant"
    ERRORS_ALIVE_TIME = 15000
    TEXT_BG_COLOR = "#00ccce"

    IP_REGEX = r"(?:\d{1,3}\.){3}\d{1,3}"
    MAC_REGEX = r"(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"
    NORMAL_REQUEST_HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like \
Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    HTTP_OK = 200

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
        self.root.maxsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.root.title(self.TITLE)
        self.root.configure(width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, bg='skyblue')

        # Main results frame
        self.main_frame = tk.Frame(self.root, width=int(self.WINDOW_WIDTH * 0.65), height=int(self.WINDOW_HEIGHT * 0.7),
                                   bg="#00cccc")
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.main_frame.grid_propagate(False)

        # Errors frame
        self.error_frame = tk.Frame(self.root, width=int(self.WINDOW_WIDTH * 0.3), height=int(self.WINDOW_HEIGHT * 0.7),
                                    bg="black")
        self.error_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.error_frame.grid_propagate(False)

        # input text box
        self.tb_input = tk.Entry(self.root)
        self.tb_input.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

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
        # Fixing lines that are longer than 23 characters, in order to fit in the frame.
        error_message = "\n".join(re.findall(".{1,23}", error_message.replace("\n", " ")))

        label = tk.Label(self.error_frame, text=error_message, relief=tk.RAISED, bg="black", fg="red")
        label.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        label.after(Assitant.ERRORS_ALIVE_TIME, label.destroy)

    def add_button(self, text, func):
        if self.buttons >= 10:
            self.show_error("You can't add more than 10 buttons.")
            return
        self.buttons += 1

        btn = tk.Button(self.root, text=text, padx=2, pady=2, command=func)
        btn.grid(row=(self.buttons - 1) % 5 + 1, column=int(self.buttons / 6), sticky=tk.N+tk.S+tk.E+tk.W, padx=5,
                 pady=1)

    def add_text_to_main_frame(self, text, height, bg=TEXT_BG_COLOR):
        text_obj = tk.Text(self.main_frame, height=height, width=50, bg=bg)
        text_obj.insert(tk.INSERT, text)
        text_obj.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        return text_obj
