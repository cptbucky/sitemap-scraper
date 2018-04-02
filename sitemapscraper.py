import urllib.request
import re

class SitemapScraper:
    def __init__(self):
        pass

    def scrape(self, target_url):
        content = self.get_target_html_content(target_url)
        sitemap_linked_list= []
        sitemap_linked_list.append([None, target_url])
        contained_hrefs = self.parse_html_for_hrefs(content)

        for i in range(0, len(contained_hrefs)):
            sitemap_linked_list.append([1, contained_hrefs[i]])

        return sitemap_linked_list

    def get_target_html_content(self, target_url):
        req = urllib.request.Request(target_url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        html_content = response.read()
        return html_content

    def parse_html_for_hrefs(self, html_content):
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
        return urls
