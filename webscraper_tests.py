import unittest

from unittest.mock import patch, Mock, MagicMock
from webscraper import WebScraper


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.monzo_site = 'https://monzo.com/'
        self.mock_urlopen = patch('urllib.request.urlopen').start()

    def test_ensure_scraper_targets_correct_url(self):
        WebScraper().scrape(self.monzo_site)
        self.mock_urlopen.assert_called_once()
        self.assertEqual(self.mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def test_successful_scrape_reports_parent_url_in_sitemap(self):
        report = WebScraper().scrape(self.monzo_site)
        self.assertIn(self.monzo_site, report)

    def test_given_response_contains_one_link_ensure_report_contains_it(self):
        blog_url = '/blog'
        html_response_content = '<!DOCTYPE html>' \
                                '<html>' \
                                '<head></head>' \
                                '<body>' \
                                f'<a href="{blog_url}">Blog!</a>' \
                                '</body>' \
                                '</html>'
        mock_response = Mock()
        mock_response.read.side_effect = [html_response_content]
        self.mock_urlopen.return_value = mock_response
        report = WebScraper().scrape(self.monzo_site)
        self.assertIn(blog_url, report)


if __name__ == '__main__':
    unittest.main()
