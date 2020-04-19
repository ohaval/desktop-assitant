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
            if attribute == "ip":
                text += f"{'IP:'.ljust(9)}{getattr(self, attribute)}\n"
            elif attribute == "country_name":
                text += f"{'Country:'.ljust(9)}{getattr(self, attribute)}\n"
            else:
                text += f"{(attribute + ':').ljust(9)}{getattr(self, attribute)}\n"

        return text
