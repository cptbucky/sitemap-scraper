import urllib.request


class WebScraper:
    def __init__(self):
        pass

    def scrape(self, target_url):
        req = urllib.request.Request(target_url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        html_content = response.read()
        return [target_url]
