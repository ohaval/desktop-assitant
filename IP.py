class IP:
    def __init__(self, ip_data):
        for key, value in ip_data.items():
            setattr(self, key, value)

    def summary(self, level="Minimal"):
        if level == "Minimal":
            attributes = ["ip", "country_name", "isp", "company", "city"]
        else:
            attributes = []

        text = ""
        for attribute in attributes:
            text += f"{(attribute + ':').ljust(20)} {getattr(self, attribute)}\n"
        print(text)
        return text







