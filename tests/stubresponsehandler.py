from tests.stubresponse import StubResponse


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
