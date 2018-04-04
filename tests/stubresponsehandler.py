from tests.stubresponse import StubResponse


class StubResponseHandler:
    def __init__(self, hrefs_map):
        self.response_hrefs_map = hrefs_map

    def Request(self, target_url, headers={}):
        return target_url

    def urlopen(self, target_url):
        content = self.build_response_for_url(target_url)
        return StubResponse(content)

    def get_style_tags(self, parent_url):
        links_html = ""

        if parent_url in self.response_hrefs_map:
            expected_page_hrefs = self.response_hrefs_map[parent_url]

            if len(expected_page_hrefs) == 2:
                for href in expected_page_hrefs[1]:
                    links_html += f'<link rel="stylesheet" href="{href}">'

        return links_html

    def get_anchor_tags(self, parent_url):
        links_html = ""

        if parent_url in self.response_hrefs_map:
            expected_page_hrefs = self.response_hrefs_map[parent_url]

            for href in expected_page_hrefs[0]:
                links_html += f'<a href="{href}">random-text!</a>'

        return links_html

    def build_response_for_url(self, parent_url):
        html_content = '<!DOCTYPE html><html>' \
                          f'<head>{self.get_style_tags(parent_url)}</head>' \
                          f'<body>{self.get_anchor_tags(parent_url)}</body>' \
                          '</html>'

        return html_content.encode('utf-8')
