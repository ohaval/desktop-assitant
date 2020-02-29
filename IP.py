class IP:
    def __init__(self, ip_data):
        for key, value in ip_data.items():
            setattr(self, key, value)

    def minimal_info(self):
        keys = ["country_name", "isp", "company", "city"]
        info = {}
        for key in keys:
            info.update({key: getattr(self, key)})

        return info


