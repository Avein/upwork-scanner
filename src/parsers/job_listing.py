from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from models.job_listing import Job, Profile
from page_objects import job_listing as job_page_object
from parsers import Parser


class JobParser(Parser):
    @staticmethod
    def get_posted_time(element: Tag) -> Optional[str]:
        posted_time = element.select(job_page_object.job_posted_time_selector.value)
        if posted_time:
            return posted_time[0].time.text
        return None

    @staticmethod
    def get_job_location_requirements(element: Tag) -> Optional[str]:
        for span in element.select(
            job_page_object.job_location_requirement_selector.value
        ):
            if "location-icon" not in span.attrs["class"]:
                return span.text
        return None

    @staticmethod
    def is_job_verified(element: Tag) -> bool:
        return (
            True
            if element.select(job_page_object.is_verified_selector.value)
            else False
        )

    @staticmethod
    def get_required_skills(element: Tag) -> List[str]:
        skills = []
        for skill in element.select(job_page_object.skills_required_selector.value):
            skills.append(skill.text)
        return skills

    @classmethod
    def parse(cls, soup: BeautifulSoup) -> List[Job]:
        # TODO REMOVE `-` FROM OCCURRING
        jobs = []
        jobs_list = soup.select(job_page_object.jobs_selector.value)

        for job_element in jobs_list:
            jobs.append(
                Job(
                    title=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_title_selector
                    ),
                    type=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_type_selector
                    ),
                    tier=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_tier_selector
                    ),
                    budget=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_budget_selector
                    ),
                    duration=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_duration_selector
                    ),
                    description=cls.get_fist_element_text_if_exist(
                        job_element, job_page_object.job_description
                    ),
                    posted_time=cls.get_posted_time(job_element),
                    location_requirement=cls.get_job_location_requirements(job_element),
                    is_verified=cls.is_job_verified(job_element),
                    skills_required=cls.get_required_skills(job_element),
                )
            )
        return jobs


class ProfileParser(Parser):
    @staticmethod
    def get_categories(element: Tag) -> List[str]:
        categories = []
        for category in element.select(job_page_object.categories_selector.value):
            categories.append(category.text)
        return categories

    @classmethod
    def parse(cls, soup: BeautifulSoup) -> Profile:

        return Profile(
            categories=cls.get_categories(soup),
            visibility=cls.get_fist_element_text_if_exist(
                soup, job_page_object.visibility_selector
            ),
            availability=cls.get_fist_element_text_if_exist(
                soup, job_page_object.availability_selector
            ),
            profile_completion=cls.get_fist_element_text_if_exist(
                soup, job_page_object.profile_completion_selector
            ),
            available_connections=cls.get_fist_element_text_if_exist(
                soup, job_page_object.available_connections_selector
            ),
        )
