import unittest

from unittest.mock import patch, Mock
from src.sitemapcli.sitemapscraper import SitemapScraper


# things to consider
#     limit the depth of a crawl to create a small sitemap ?! probably not relevant

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

        self.assertEqual(1, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, []])

    def test_html_response_has_single_child_link_report_contains_link(self):
        blog_url = '/blog'
        self.given_stub_response({self.monzo_site: [blog_url]})

        report = self.on_scrape_url()

        self.assertEqual(2, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1]])
        self.assert_sitemap_entry_correct(report, 1, [0, blog_url, []])

    def test_html_response_has_multiple_child_links_report_contains_all_links(self):
        url_one = '/blog'
        url_two = '/contact'
        url_three = '/features'
        self.given_stub_response({self.monzo_site: [url_one, url_two, url_three]})

        report = self.on_scrape_url()

        self.assertEqual(4, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 2, 3]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, []])
        self.assert_sitemap_entry_correct(report, 2, [0, url_two, []])
        self.assert_sitemap_entry_correct(report, 3, [0, url_three, []])

    def test_html_response_single_child_has_single_child_report_links_pages(self):
        self.given_stub_response({self.monzo_site: ['/blog'], '/blog': ['/my-blog-entry']})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1]])
        self.assert_sitemap_entry_correct(report, 1, [0, '/blog', [2]])
        self.assert_sitemap_entry_correct(report, 2, [1, '/my-blog-entry', []])

    def test_html_response_has_single_child_and_external_links_report_should_contain_single_child_only(self):
        url_one = 'http://www.google.com'
        url_two = '/contact'
        url_three = 'https://www.google.co.uk/search?q=monzo'
        self.given_stub_response({self.monzo_site: [url_one, url_two, url_three]})

        report = self.on_scrape_url()

        self.assertEqual(2, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_two, []])

    def test_html_response_has_relative_and_absolute_links_report_should_contain_both(self):
        url_one = 'https://monzo.com/blog'
        url_two = '/contact'
        self.given_stub_response({self.monzo_site: [url_one, url_two]})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 2]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, []])
        self.assert_sitemap_entry_correct(report, 2, [0, url_two, []])

    def test_html_response_has_two_links_with_different_protocols_report_should_contain_both(self):
        url_one = 'https://monzo.com/blog'
        url_two = 'http://monzo.com/contact'
        self.given_stub_response({self.monzo_site: [url_one, url_two]})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 2]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, []])
        self.assert_sitemap_entry_correct(report, 2, [0, url_two, []])

    def test_html_response_has_two_links_with_different_query_strings_report_should_contain_both(self):
        url_one = 'https://monzo.com/blog?platform=mobile'
        url_two = 'https://monzo.com/blog?platform=desktop'
        self.given_stub_response({self.monzo_site: [url_one, url_two]})

        report = self.on_scrape_url()

        self.assertEqual(3, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 2]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, []])
        self.assert_sitemap_entry_correct(report, 2, [0, url_two, []])

    def test_html_response_has_duplicate_links_report_should_contain_single(self):
        url_one = 'https://monzo.com/blog'
        self.given_stub_response({self.monzo_site: [url_one, url_one]})

        report = self.on_scrape_url()

        self.assertEqual(2, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, []])

    def test_two_child_pages_contain_same_link_report_should_contain_both(self):
        url_one = 'https://monzo.com/customer-blog'
        url_two = 'https://monzo.com/tech-blog'
        url_three = 'https://monzo.com/blog/entry'
        self.given_stub_response({self.monzo_site: [url_one, url_two], url_one: [url_three], url_two: [url_three]})

        report = self.on_scrape_url()

        self.assertEqual(5, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 3]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, [2]])
        self.assert_sitemap_entry_correct(report, 2, [1, url_three, []])
        self.assert_sitemap_entry_correct(report, 3, [0, url_two, [4]])
        self.assert_sitemap_entry_correct(report, 4, [3, url_three, []])

#     recursive links - ensures the implementation stops at crawling parents but includes parent link in child page
    def test_recursive_link_structure_should_not_crawl_levels_above_and_report_should_contain_links(self):
        url_one = 'https://monzo.com/blog'
        url_two = 'https://monzo.com/blog/blog-entry'
        self.given_stub_response({self.monzo_site: [url_one, url_two], url_one: [url_two], url_two: [url_one]})

        report = self.on_scrape_url()

        self.assertEqual(7, len(report))
        self.assert_sitemap_entry_correct(report, 0, [None, self.monzo_site, [1, 4]])
        self.assert_sitemap_entry_correct(report, 1, [0, url_one, [2]])
        self.assert_sitemap_entry_correct(report, 2, [1, url_two, [3]])
        self.assert_sitemap_entry_correct(report, 3, [2, url_one, []])
        self.assert_sitemap_entry_correct(report, 4, [0, url_two, [5]])
        self.assert_sitemap_entry_correct(report, 5, [4, url_one, [6]])
        self.assert_sitemap_entry_correct(report, 6, [5, url_two, []])

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

    def assert_sitemap_entry_correct(self, report, entry_index, expected_entry):
        self.assertGreaterEqual(len(report) - 1, entry_index)
        self.assertEqual(report[entry_index][0], expected_entry[0])
        self.assertEqual(report[entry_index][1], expected_entry[1])
        self.assertEqual(report[entry_index][2], expected_entry[2])


if __name__ == '__main__':
    unittest.main()
