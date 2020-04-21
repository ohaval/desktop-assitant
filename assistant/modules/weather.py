
import requests
from bs4 import BeautifulSoup

import _set_path
from assitant import Assitant


class Weather(Assitant):
    WEATHER_URL_HAIFA = "https://www.accuweather.com/en/il/haifa/213181/weather-forecast/213181"

    def __init__(self):
        Assitant.__init__(self)
        self.TEXT_OBJECTS = []

    def start(self):
        self.add_button("Clean", self.clean_text)
        self.add_button("Current Weather", self.weather_right_now)

        self.root.mainloop()

    def clean_text(self):
        for text_obj in self.TEXT_OBJECTS:
            text_obj.destroy()
        self.TEXT_OBJECTS = []

    def weather_right_now(self):
        page = requests.get(self.WEATHER_URL_HAIFA, headers=Assitant.NORMAL_REQUEST_HEADERS)
        if page.status_code != Assitant.HTTP_OK:
            self.show_error(f"Response error ({page.status_code})")
            return

        try:
            soup = BeautifulSoup(page.content, 'lxml')
            today_block = soup.find('div', class_='day-panel')
            temp = today_block.find('span', class_='high').text.strip("\t\n")
            desc = today_block.find('div', class_='cond').text.strip()
        except AttributeError:
            self.show_error("Error encountered when parsing the page content.")
            return

        text = f"Temperature: {temp}\n{desc}\n"
        self.TEXT_OBJECTS.append(self.add_text_to_main_frame(text, text.count("\n")))


def main():
    obj = Weather()
    obj.start()


if __name__ == "__main__":
    main()
