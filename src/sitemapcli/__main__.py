# from . import sitemapscraper
# from . import sitemapconsolewriter
from src.sitemapcli import sitemapscraper


def main():
    site_to_scrape = "https://monzo.com/"
    scraper = sitemapscraper.SitemapScraper(site_to_scrape)
    scraper.scrape()
    print("hello")


if __name__ == '__main__':
    main()
