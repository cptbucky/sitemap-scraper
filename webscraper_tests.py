import unittest

from unittest.mock import patch, Mock, MagicMock
from webscraper import WebScraper


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.scrape_url = 'https://monzo.com/'
        self.subject = WebScraper()

    @patch('urllib.request.urlopen')
    def test_ensure_scraper_targets_correct_url(self, mock_urlopen):
        self.when_scraping_site()
        mock_urlopen.assert_called_once_with(self.scrape_url)

    @patch('urllib.request.urlopen')
    def test_successful_scrape_reports_parent_url_in_sitemap(self, mock_urlopen):
        report = self.when_scraping_site()
        self.assertIn(self.scrape_url, report)

    def when_scraping_site(self):
        return self.subject.scrape(self.scrape_url)


if __name__ == '__main__':
    unittest.main()
