from dataclasses import dataclass
from typing import Optional

from loguru import logger
from undetected_chromedriver import Chrome

from helpers import find_element_by, wait_to_load
from models.profile_settings import Address
from page_objects import contact_info as ci_po
from parsers import Parser


@dataclass
class ContactInfo:
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_info_address: Optional[Address] = None


class ContactInfoParser(Parser):
    @staticmethod
    def get_email_address(driver: Chrome) -> str:
        logger.debug("Parsing email address")
        email_input = wait_to_load(driver, ci_po.email_input_selector)
        return email_input.get_attribute("value")

    @staticmethod
    def get_address(driver: Chrome) -> Address:
        logger.debug("Parsing user address")
        line_1 = wait_to_load(driver, ci_po.address1_span_selector)
        return Address(
            line_1=line_1.text,
            line_2=find_element_by(driver, ci_po.address2_span_selector).text,
            postal_code=find_element_by(driver, ci_po.zip_span_selector).text,
            city=find_element_by(driver, ci_po.city_span_selector).text,
            state=find_element_by(driver, ci_po.state_span_selector).text,
            country=find_element_by(driver, ci_po.country_span_selector).text,
        )

    @staticmethod
    def get_phone_number(driver: Chrome) -> str:
        logger.debug("Parsing phone number")
        phone_number = wait_to_load(driver, ci_po.phone_span_selector)
        return phone_number.text

    @classmethod
    def parse(cls, driver: Chrome) -> ContactInfo:
        return ContactInfo(
            contact_info_address=cls.get_address(driver),
            phone_number=cls.get_phone_number(driver),
            email_address=cls.get_email_address(driver),
        )
