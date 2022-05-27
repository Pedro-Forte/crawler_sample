import scrapy
from ..items import CialdnbItem
from urllib.parse import urlparse
import re


class BasicInfoSpider(scrapy.Spider):
    name = 'basic_info'
    start_urls = ['https://www.illion.com.au/contact-us/']

    def parse(self, response, **kwargs):

        item = CialdnbItem()

        item["logo"] = self.find_logo(response)
        item["website"] = response.url
        item["phones"] = self.find_phones(response)

        yield item

    def find_logo(self, response):
        # Return absolute URL for logo

        match_logo = ""
        blank_logo = ""

        logo_try = [response.xpath("//img[re:test(@id, '[lL][oO][gG][oO]')]/@src").getall(),
                    response.xpath("//img[re:test(@class, '[lL][oO][gG][oO]')]/@src").getall(),
                    response.xpath("//img[re:test(@src, '[lL][oO][gG][oO]')]/@src").getall()]

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

    def find_phones(self, response):

        phones = []

        phones_try = [response.xpath("//*[re:test(@class, 'contact')]/text()").getall(),
                      response.xpath("//*[re:test(@href, 'tel:')]/text()").getall(),
                      response.xpath("//*[re:test(@href, 'phone')]/text()").getall(),
                      response.xpath("//*[re:test(@href, '//+')]/text()").getall()]

        for phones_list in phones_try:
            for phone in phones_list:
                phone_verification = phone.replace("+", " ").replace("/", " ")
                phone_verification = ''.join(c for c in phone_verification if c.isdigit() or c == " " or c == "("
                                             or c == ")")
                if phone_verification.replace(" ", "") and len(phone_verification.replace(" ", "")) > 6:
                    phones.append(phone_verification)

        return phones
