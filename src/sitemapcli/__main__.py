from . import sitemapscraper
from . import sitemapconsolewriter
# from src.sitemapcli import sitemapscraper
# from src.sitemapcli import sitemapconsolewriter


def main():
    site_to_scrape = "https://monzo.com/"
    scraper = sitemapscraper.SitemapScraper(site_to_scrape, 20)
    sitemap = scraper.scrape()
    writer = sitemapconsolewriter.TreeConsoleWriter()
    writer.write(sitemap)


if __name__ == '__main__':
    main()
