import scrapy
from ..items import CialdnbItem
from urllib.parse import urlparse


class BasicInfoSpider(scrapy.Spider):
    name = 'basic_info'
    # allowed_domains = ['www.cialdnb.com']
    start_urls = ['https://www.unilever.com.br/']

    def parse(self, response, **kwargs):

        item = CialdnbItem()

        item["logo"] = self.find_logo(response)

        yield item

    def find_logo(self, response):
        # Return absolute URL for logo

        match_logo = ""
        blank_logo = ""

        logo_try = [response.xpath("//img[re:test(@id, 'logo')]/@src").getall(),
                    response.xpath("//img[re:test(@class, 'logo')]/@src").getall(),
                    response.xpath("//img[re:test(@src, 'logo')]/@src").getall()]

        for logo_list in logo_try:
            for logo in logo_list:
                blank_logo = logo
                if "logo" in logo and ("color" in logo.lower() or "coloured" in logo.lower() or "rgb" in logo.lower()):
                    # Verify if exist more than one logo and is blank
                    match_logo = logo
                    break

            if not match_logo:
                # If the logo is not tagged with 'color' match logo should receive the right one
                match_logo = blank_logo

            if match_logo:
                verify_absolute_url = urlparse(match_logo)

                if not verify_absolute_url.hostname:
                    base_url = urlparse(response.url)
                    match_logo = f"{base_url.scheme}://{base_url.hostname}{match_logo}"

                break

        return match_logo

    def find_phone(self, response):

        pass
