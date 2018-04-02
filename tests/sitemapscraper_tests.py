import unittest

from unittest.mock import patch, Mock
from src.sitemapscraper import SitemapScraper


# things to consider
#     ensure page hrefs are crawled ^
#     ignore protocol ^
#     query strings as different pages
#     de-dupe links
#     recursive links - ensure following considers existing crawls/results
#         use a linked list to the parent url index and the url itself [parent-index, url]
#     limit the depth of a crawl to create a small sitemap ?! probably not relevant
#     create an iprinter that can be swapped out for file output

from tests.stubresponsehandler import StubResponseHandler


class SitemapScraperTests(unittest.TestCase):

    def setUp(self):
        self.monzo_site = 'https://monzo.com/'

    def test_ensure_scraper_crawls_target_page(self):
        mock_urlopen = self.given_mock_response()

        self.on_scrape_url()

        mock_urlopen.assert_called_once()
        self.assertEqual(mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def test_successful_scrape_reports_parent_url_in_sitemap(self):
        self.given_stub_response({self.monzo_site: []})

        report = self.on_scrape_url()

        self.assertIn(self.monzo_site, report[0])

    def test_html_response_has_single_child_link_expect_returned(self):
        url_one = '/blog'
        url_two = '/contact'
        url_three = '/features'
        self.given_stub_response({self.monzo_site: [url_one, url_two, url_three]})

        report = self.on_scrape_url()

        self.assertIn(url_one, report[1])
        self.assertIn(url_two, report[2])
        self.assertIn(url_three, report[3])

    def test_html_response_has_multiple_children_link_expect_returned(self):
        blog_url = '/blog'
        self.given_stub_response({self.monzo_site: [blog_url]})

        report = self.on_scrape_url()

        self.assertIn(blog_url, report[1])

    def test_html_response_single_child_has_single_child_report_has_correct_levels(self):
        self.given_stub_response({self.monzo_site: ['/blog'], '/blog': ['/my-blog-entry']})

        report = self.on_scrape_url()

        self.assertEqual(0, report[1][0])
        self.assertEqual('/blog', report[1][1])
        self.assertEqual(1, report[2][0])
        self.assertEqual('/my-blog-entry', report[2][1])

    def test_html_response_has_single_child_and_external_links_report_should_contain_single_child_only(self):
        url_one = 'http://www.google.com'
        url_two = '/contact'
        url_three = 'https://www.google.co.uk/search?q=monzo'
        self.given_stub_response({self.monzo_site: [url_one, url_two, url_three]})

        report = self.on_scrape_url()

        self.assertEqual(2, len(report))
        self.assertIn(url_two, report[1])

    def test_html_response_has_relative_and_absolute_links_report_should_contain_both(self):
        url_one = 'https://monzo.com/blog'
        url_two = '/contact'
        self.given_stub_response({self.monzo_site: [url_one, url_two]})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assertEqual(url_one, report[1][1])
        self.assertEqual(url_two, report[2][1])

    def test_html_response_has_two_links_with_different_protocols_report_should_contain_both(self):
        url_one = 'https://monzo.com/blog'
        url_two = 'http://monzo.com/contact'
        self.given_stub_response({self.monzo_site: [url_one, url_two]})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assertEqual(url_one, report[1][1])
        self.assertEqual(url_two, report[2][1])

    def on_scrape_url(self):
        return SitemapScraper(self.monzo_site).scrape()

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
