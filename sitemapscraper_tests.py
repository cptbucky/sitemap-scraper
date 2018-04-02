import unittest

from unittest.mock import patch, Mock, MagicMock
from sitemapscraper import SitemapScraper


# things to consider
#     query strings as different pages
#     de-dupe links
#     recursive links - ensure following considers existing crawls/results
#         use a linked list to the parent url index and the url itself [parent-index, url]
#     limit the depth of a crawl to create a small sitemap ?! probably not relevant
#     create an iprinter that can be swapped out for file output
#     ensure page hrefs are crawled


class SitemapScraperTests(unittest.TestCase):

    def setUp(self):
        self.monzo_site = 'https://monzo.com/'
        self.mock_urlopen = patch('urllib.request.urlopen').start()

    def test_ensure_scraper_targets_correct_url(self):
        self.given_response()
        SitemapScraper().scrape(self.monzo_site)
        self.mock_urlopen.assert_called_once()
        self.assertEqual(self.mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def test_successful_scrape_reports_parent_url_in_sitemap(self):
        self.given_response()
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(self.monzo_site, report[0])

    def test_html_response_has_single_child_link_expect_returned(self):
        blog_url = '/blog'
        self.given_response_with_links([blog_url])
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(blog_url, report[1])

    def given_response_with_links(self, links):
        html_response_content = '<!DOCTYPE html>' \
                                '<html>' \
                                '<head></head>' \
                                '<body>' \
                                f'<a href="{links[0]}">Blog!</a>' \
                                '</body>' \
                                '</html>'
        mock_response = Mock()
        mock_response.read.side_effect = [html_response_content]
        self.mock_urlopen.return_value = mock_response

    def given_response(self):
        mock_response = Mock()
        mock_response.read.side_effect = [""]
        self.mock_urlopen.return_value = mock_response


if __name__ == '__main__':
    unittest.main()
