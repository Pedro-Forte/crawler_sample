import scrapy
from ..items import CialdnbItem
from urllib.parse import urlparse
import re


class BasicInfoSpider(scrapy.Spider):
    name = 'basic_info'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = kwargs["domain"]

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
        char_to_replace = {
            "+": " ",
            "/": " ",
            "-": " "
        }

        phone_converter = {
            "a": "2", "b": "2", "c": "2", "d": "3", "e": "3", "f": "3", "g": "4", "h": "4", "i": "4", "j": "5",
            "k": "5", "l": "5", "m": "6", "n": "6", "o": "6", "p": "7", "q": "7", "r": "7", "s": "7", "t": "8",
            "u": "8", "v": "8", "w": "9", "x": "9", "y": "9", "z": "9"
        }

        phones_try = [response.xpath("//*[re:test(@class, 'contact')]/text()").getall(),
                      response.xpath("//*[re:test(@href, 'tel:')]/text()").getall(),
                      response.xpath("//*[re:test(@href, 'phone')]/text()").getall(),
                      response.xpath("//*[re:test(@href, '//+')]/text()").getall()]

        for phones_list in phones_try:
            for phone in phones_list:
                # Replace +/- to " " using char_to_replace dict
                phone_verification = re.sub(r"[+/-]",
                                            lambda x: char_to_replace[x.group(0)],
                                            phone)

                if "0800 " in phone_verification:
                    # This regex convert words to phone numbers
                    phone_verification = re.sub(r"[a-z]",
                                                lambda x: phone_converter[x.group(0)],
                                                phone_verification.lower())

                # Remove non numeric/parentheses/" " chars
                phone_verification = re.sub("[^0-9() ]", "", phone_verification)

                if len(phone_verification.replace(" ", "")) > 6:
                    # less than 6 char isnt considered as phone number
                    phones.append(phone_verification)

        return phones
