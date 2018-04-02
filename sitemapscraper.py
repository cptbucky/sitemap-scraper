import urllib.request
import re


class SitemapScraper:
    # inject interface for network request?
    def __init__(self):
        pass

    def scrape(self, target_url):
        sitemap_linked_list = [[None, target_url]]

        self.scrape_target(sitemap_linked_list, 0, target_url)

        return sitemap_linked_list

    def scrape_target(self, sitemap, parent_index, target_url):
        content = self.get_target_html_content(target_url)
        contained_hrefs = self.parse_html_for_hrefs(content)

        for i in range(0, len(contained_hrefs)):
            child_url = contained_hrefs[i]
            sitemap.append([parent_index, child_url])
            self.scrape_target(sitemap, parent_index + 1, child_url)

    @staticmethod
    def get_target_html_content(target_url):
        req = urllib.request.Request(target_url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        html_content = response.read()
        return html_content

    @staticmethod
    def parse_html_for_hrefs(html_content):
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
        return urls
