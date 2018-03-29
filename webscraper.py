import urllib.request


class WebScraper:
    def __init__(self):
        pass

    def scrape(self, target_url):
        response = urllib.request.urlopen(target_url)
        return [target_url]
