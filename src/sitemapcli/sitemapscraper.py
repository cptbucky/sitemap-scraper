import urllib.request
import re

from urllib.parse import urlsplit


class SitemapScraper:
    def __init__(self, base_url, url_limit=100):
        self.url_limit = url_limit
        self.__base_url = base_url.strip('/')
        self.__url_matcher = re.compile(
            r'([A-Za-z]{3,9})://([-;:&=\+\$,\w]+@{1})?([-A-Za-z0-9\.]+)+:?(\d+)?((/[-\+~%/\.\w]+)?\??([-\+=&;%@\.\w]+)?#?([\w]+)?)?'
        )
        self.__anchor_tag_matcher = re.compile(
            r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
        )

    def scrape(self):
        sitemap = [[None, self.__base_url, []]]

        self.__scrape_target(sitemap, self.__base_url, 0)

        return sitemap

    def __scrape_target(self, sitemap, target_url, parent_index):
        content = self.__get_target_html_content(target_url)
        html_content = str(content, 'utf-8')
        contained_hrefs = self.__parse_html_for_hrefs(html_content)

        for child_link in contained_hrefs:
            if self.__external_link(child_link):
                continue

            # descoping traversing of paths
            if self.__requires_traversing(child_link):
                continue

            absolute_child_link = self.__to_absolute_path(child_link)

            if not self.__valid_url(absolute_child_link):
                continue

            if self.__link_exists_in_current_page(sitemap, absolute_child_link, parent_index):
                continue

            sitemap.append([parent_index, absolute_child_link, []])
            child_index = len(sitemap) - 1
            sitemap[parent_index][2].append(child_index)

            if self.__link_exists_as_parent_page(sitemap, absolute_child_link, parent_index):
                continue

            if len(sitemap) > self.url_limit:
                return

            self.__scrape_target(sitemap, absolute_child_link, child_index)

    @staticmethod
    def __get_target_html_content(target_url):
        req = urllib.request.Request(target_url, headers={'User-Agent': "Magic Browser"})
        response = urllib.request.urlopen(req)
        html_content = response.read()
        return html_content

    def __parse_html_for_hrefs(self, html_content):
        urls = self.__anchor_tag_matcher.findall(html_content)
        return urls

    def __external_link(self, child_url):
        url = urlsplit(child_url)
        internal_url = (url.netloc == '') or (url.netloc == urlsplit(self.__base_url).netloc)
        return not internal_url

    def __valid_url(self, child_url):
        # being pretty stringent here, url must include protocol
        is_valid_url = self.__url_matcher.match(child_url)
        return is_valid_url

    @staticmethod
    def __requires_traversing(child_url):
        return child_url.startswith('.')

    @staticmethod
    def __link_exists_in_current_page(sitemap, child_url, parent_index):
        found_exact_match = False

        for i in range(0, len(sitemap)):
            if sitemap[i][0] == parent_index and sitemap[i][1] == child_url:
                return True

        return found_exact_match

    def __link_exists_as_parent_page(self, sitemap, child_url, parent_index):
        if parent_index is None:
            return False

        if sitemap[parent_index][1] == child_url:
            return True
        else:
            return self.__link_exists_as_parent_page(sitemap, child_url, sitemap[parent_index][0])

    def __to_absolute_path(self, url):
        if url.startswith('/'):
            return f"{self.__base_url}{url}".strip('/')
        else:
            return url
