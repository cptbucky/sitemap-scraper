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
        self.mock_urlopen = patch('urllib.request.urlopen').start()

    def test_ensure_scraper_crawls_target_page(self):
        self.given_response_empty(self.monzo_site)
        SitemapScraper().scrape(self.monzo_site)
        self.mock_urlopen.assert_called_once()
        self.assertEqual(self.mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def test_successful_scrape_reports_parent_url_in_sitemap(self):
        self.given_response_empty(self.monzo_site)
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(self.monzo_site, report[0])

    def test_html_response_has_single_child_link_expect_returned(self):
        url_one = '/blog'
        url_two = '/contact'
        url_three = '/features'
        self.given_response_with_links(self.monzo_site, [url_one, url_two, url_three])
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(url_one, report[1])
        self.assertIn(url_two, report[2])
        self.assertIn(url_three, report[3])

    def test_html_response_has_multiple_children_link_expect_returned(self):
        blog_url = '/blog'
        self.given_response_with_links(self.monzo_site, [blog_url])
        report = SitemapScraper().scrape(self.monzo_site)
        self.assertIn(blog_url, report[1])

    def test_ensure_scraper_crawls_child_pages(self):
        self.given_response_with_links(self.monzo_site, ['/blog'])
        SitemapScraper().scrape(self.monzo_site)
        self.mock_urlopen.assert_called_once()
        self.assertEqual(self.mock_urlopen.call_args[0][0].full_url, self.monzo_site)

    def given_response_empty(self, parent_url):
        self.given_response(parent_url, "")

    def given_response_with_links(self, parent_url, links):
        html_start_tags = '<!DOCTYPE html>' \
                                '<html>' \
                                '<head></head>' \
                                '<body>'

        links_html = ""

        for i in range(0, len(links)):
            links_html += f'<a href="{links[i]}">random-text!</a>'

        html_end_tags = '</body>' \
                        '</html>'

        self.given_response(html_start_tags + links_html + html_end_tags)

    def given_response(self, parent_url, response):
        mock_response = Mock()
        mock_response.read.side_effect = [response]
        self.mock_urlopen.return_value = mock_response


if __name__ == '__main__':
    unittest.main()
