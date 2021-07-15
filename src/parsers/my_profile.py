from dataclasses import dataclass, field
from typing import List, Optional

from loguru import logger
from undetected_chromedriver import Chrome

from helpers import find_elements_by, wait_to_load
from models.profile_settings import Employment
from page_objects import my_profile as ms_po
from parsers import Parser


@dataclass
class MyProfile:
    profile_picture_url: Optional[str] = None
    present_employments: List[Employment] = field(default_factory=list)


class MyProfileParser(Parser):
    @staticmethod
    def get_present_employments(driver: Chrome) -> List[Employment]:
        logger.debug("Parsing employment history")
        employments = []
        employments_list = find_elements_by(driver, ms_po.employment_list_selector)

        for employment in employments_list:
            data = employment.find_element_by_css_selector("div.mt-10.text-muted").text
            start_data, end_date = data.strip().split("-")

            if end_date.strip() == "Present":

                data = employment.find_element_by_css_selector("h4").text
                position, employer_name = data.split("|")

                employments.append(
                    Employment(
                        employer_name=employer_name,
                        position=position,
                        start_date=start_data,
                        end_date=end_date,
                    )
                )
        return employments

    @staticmethod
    def get_user_picture_url(driver: Chrome) -> str:
        logger.debug("Parsing profile picture url")
        data = wait_to_load(driver, ms_po.profile_image_url_selector)
        return data.get_attribute("src")

    @classmethod
    def parse(cls, driver: Chrome) -> MyProfile:

        return MyProfile(
            profile_picture_url=cls.get_user_picture_url(driver),
            present_employments=cls.get_present_employments(driver),
        )
