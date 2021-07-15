from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import Chrome

from config import TimeoutsEnum
from enums import JobListStagesEnum
from helpers import click_with_move, wait_to_load
from page_objects import Selector
from page_objects import job_listing as job_po
from parsers.job_listing import JobParser, ProfileParser
from stages import Stage, StageResult


@dataclass
class JobListMultiStage(Stage):
    selector: Selector = job_po.jobs_selector
    multi_stage_result: List[StageResult] = field(default_factory=lambda: list())
    multi_stage_name: JobListStagesEnum = JobListStagesEnum.MULTISTAGE_1_JOB_LIST

    def load_more_jobs(self, last_jobs_no: int = 20) -> None:
        def _get_no_loaded_jobs(driver: Chrome) -> int:
            return len(driver.find_elements_by_css_selector(job_po.jobs_selector.value))

        def _close_job_details(driver: Chrome) -> None:
            try:
                wait_to_load(driver, job_po.submit_job_proposal_button_selector)
                driver.back()
            except TimeoutException:
                pass

        def _find_load_more_jobs_button(driver: Chrome) -> Optional[WebElement]:

            # scrolling down to load all pages
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                load_more_button = wait_to_load(
                    driver,
                    job_po.load_more_jobs_button_selector,
                    timeout=TimeoutsEnum.MEDIUM,
                )
                return load_more_button
            except TimeoutException:
                return None

        stage_name = JobListStagesEnum.STAGE_0_LOAD_JOBS_LIST
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        while True:
            no_loaded_jobs = _get_no_loaded_jobs(self.driver)
            if no_loaded_jobs < last_jobs_no:

                load_more_button = _find_load_more_jobs_button(self.driver)
                if load_more_button:
                    click_with_move(self.driver, web_element=load_more_button)
                else:
                    logger_msg = (
                        f"No more jobs to load. " f"{no_loaded_jobs} jobs loaded"
                    )
                    logger.info(logger_msg)
                    self.update_result(stage_result, msg=logger_msg)
                    break
            else:
                logger_msg = f"Min. {no_loaded_jobs} jobs loaded"
                logger.info(logger_msg)
                self.update_result(stage_result, msg=logger_msg)
                break

        _close_job_details(self.driver)
        self.multi_stage_result.append(stage_result)

    def parse_jobs_list(self, soup: BeautifulSoup) -> None:
        stage_name = JobListStagesEnum.STAGE_1_SCRAPE_JOBS_LIST
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        jobs = JobParser.parse(soup)

        self.update_result(
            stage_result, msg="Successfully parsed jobs list", parsed_data_list=jobs
        )
        self.multi_stage_result.append(stage_result)
        logger.debug("Successfully parsed jobs list")

    def parse_profile(self, soup: BeautifulSoup) -> None:
        stage_name = JobListStagesEnum.STAGE_2_SCRAPE_PROFILE
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        profile = ProfileParser.parse(soup)

        logger_msg = "Successfully parsed profile info on job list page"
        self.update_result(stage_result, msg=logger_msg, parsed_data=profile)
        self.multi_stage_result.append(stage_result)
        logger.debug(logger_msg)

    def do_action(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        logger.info(f"Starting multistage: {self.multi_stage_name}")
        stage_result = self.init_result(
            stage_name=self.multi_stage_name, ip_address=self.ip_address
        )

        self.load_more_jobs()  # STAGE 0

        soup = BeautifulSoup(self.driver.page_source, features="html.parser")

        self.parse_jobs_list(soup)  # STAGE 1
        self.parse_profile(soup)  # STAGE 2

        logger.info(f"Ending multistage: {self.multi_stage_name} with success")
        self.update_result(
            stage_result, msg="Successfully parsed jobs and profile data"
        )
        self.multi_stage_result.append(stage_result)
