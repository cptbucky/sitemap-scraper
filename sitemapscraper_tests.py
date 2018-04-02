import unittest

from unittest.mock import patch, Mock, MagicMock
from sitemapscraper import SitemapScraper


# things to consider
#     ensure page hrefs are crawled
#     query strings as different pages
#     de-dupe links
#     recursive links - ensure following considers existing crawls/results
#         use a linked list to the parent url index and the url itself [parent-index, url]
#     limit the depth of a crawl to create a small sitemap ?! probably not relevant
#     create an iprinter that can be swapped out for file output


class SitemapScraperTests(unittest.TestCase):

    def setUp(self):
        self.monzo_site = 'https://monzo.com/'

    def test_ensure_scraper_crawls_target_page(self):
        mock_urlopen = self.given_mock_response()
        SitemapScraper().scrape(self.monzo_site)
        mock_urlopen.assert_called_once()
        self.assertEqual(mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def test_successful_scrape_reports_parent_url_in_sitemap(self):
        self.given_stub_response({self.monzo_site: []})
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(self.monzo_site, report[0])

    def test_html_response_has_single_child_link_expect_returned(self):
        url_one = '/blog'
        url_two = '/contact'
        url_three = '/features'
        self.given_stub_response({self.monzo_site: [url_one, url_two, url_three]})
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(url_one, report[1])
        self.assertIn(url_two, report[2])
        self.assertIn(url_three, report[3])

    def test_html_response_has_multiple_children_link_expect_returned(self):
        blog_url = '/blog'
        self.given_stub_response({self.monzo_site: [blog_url]})
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(blog_url, report[1])

    def test_html_response_single_child_has_single_child_report_has_correct_levels(self):
        self.given_stub_response({self.monzo_site: ['/blog'], '/blog': ['/my-blog-entry']})
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertEqual(0, report[1][0])
        self.assertEqual('/blog', report[1][1])
        self.assertEqual(1, report[2][0])
        self.assertEqual('/my-blog-entry', report[2][1])

    @staticmethod
    def given_mock_response():
        mock_urlopen = patch('urllib.request.urlopen').start()
        mock_response = Mock()
        mock_response.read.side_effect = [""]
        mock_urlopen.return_value = mock_response
        return mock_urlopen

    @staticmethod
    def given_stub_response(links_by_url):
        mock_urlrequest = patch('urllib.request').start()
        handler = StubResponseHandler(links_by_url)
        mock_urlrequest.Request.side_effect = handler.Request
        mock_urlrequest.urlopen.side_effect = handler.urlopen


if __name__ == '__main__':
    unittest.main()


class StubResponseHandler:
    def __init__(self, links_by_url):
        self.response_map = links_by_url

    def Request(self, target_url, headers={}):
        return target_url

    def urlopen(self, target_url):
        content = self.build_response_for_url(target_url)
        return StubResponse(content)

    def build_response_for_url(self, parent_url):
        html_start_tags = '<!DOCTYPE html>' \
                                '<html>' \
                                '<head></head>' \
                                '<body>'

        links_html = ""

        if parent_url in self.response_map:
            for i in range(0, len(self.response_map[parent_url])):
                links_html += f'<a href="{self.response_map[parent_url][i]}">random-text!</a>'

        html_end_tags = '</body>' \
                        '</html>'

        return html_start_tags + links_html + html_end_tags


class StubResponse:
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content
