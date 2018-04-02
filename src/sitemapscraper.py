import urllib.request
import re

from urllib.parse import urlsplit


class SitemapScraper:
    # inject interface for network request?
    def __init__(self, base_url):
        self.__base_url = base_url

    def scrape(self):
        sitemap_linked_list = [[None, self.__base_url]]

        self.__scrape_target(sitemap_linked_list, 0, self.__base_url)

        return sitemap_linked_list

    def __scrape_target(self, sitemap, parent_index, target_url):
        content = self.__get_target_html_content(target_url)
        contained_hrefs = self.__parse_html_for_hrefs(content)

        for i in range(0, len(contained_hrefs)):
            child_url = contained_hrefs[i]

            if self.__external_link(child_url):
                continue

            if self.__sitemap_contains_url(sitemap, child_url, parent_index):
                continue

            sitemap.append([parent_index, child_url])
            self.__scrape_target(sitemap, parent_index + 1, child_url)

    @staticmethod
    def __get_target_html_content(target_url):
        req = urllib.request.Request(target_url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        html_content = response.read()
        return html_content

    @staticmethod
    def __parse_html_for_hrefs(html_content):
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
        return urls

    def __external_link(self, child_url):
        url = urlsplit(child_url)
        internal_url = (url.netloc == '') or (url.netloc == urlsplit(self.__base_url).netloc)
        return not internal_url

    @staticmethod
    def __sitemap_contains_url(sitemap, child_url, parent_index):
        found_exact_match = False

        for i in range(0, len(sitemap)):
            if sitemap[i][0] == parent_index and sitemap[i][1] == child_url:
                return True

        return found_exact_match
