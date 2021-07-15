import os
from dataclasses import dataclass, field
from time import sleep
from typing import List

import requests
from loguru import logger
from requests import HTTPError
from selenium.common.exceptions import TimeoutException

from credential import User
from enums import ProfileSettingsStagesEnum
from helpers import click_with_move, wait_to_load
from models.profile_settings import ProfileSettings
from page_objects import contact_info as ci_po
from page_objects import my_profile as ms_po
from page_objects import profile_settings as ps_po
from parsers.certificate_of_earnings_pdf import PDFData, PDFParser
from parsers.contact_info import ContactInfo, ContactInfoParser
from parsers.my_profile import MyProfile, MyProfileParser
from stages import Stage, StageResult
from stages.login import TFAStage
from utils import base_path


@dataclass
class ProfileSettingsMultiStage(Stage):
    multi_stage_result: List[StageResult] = field(default_factory=lambda: list())
    multi_stage_name: ProfileSettingsStagesEnum = ProfileSettingsStagesEnum.MULTISTAGE_2_PROFILE_SETTINGS

    pdf_download_path = os.path.join(
        base_path, "download", "certificate_of_earnings.pdf"
    )

    def download_pdf(self) -> StageResult:
        stage_name = ProfileSettingsStagesEnum.STAGE_0_DOWNLOAD_CERTIFICATE_PDF
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        cookies = self.driver.get_cookies()

        #  parse cookies to requests format
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])

        try:
            # download pdf
            response = session.get(url=ps_po.certificate_of_earnings_url)

            response.raise_for_status()
            with open(self.pdf_download_path, "wb") as f:
                f.write(response.content)

            logger_msg = (
                f"Successfully downloaded pdf file into: " f"{self.pdf_download_path}"
            )
            logger.info(logger_msg)
            self.update_result(stage_result, msg=logger_msg)

        except HTTPError as e:
            logger_msg = f"Download ended with error: {e}"
            logger.info(logger_msg)
            self.update_result(stage_result, msg=logger_msg, result_status=False)

        finally:
            self.multi_stage_result.append(stage_result)

        return stage_result

    def parse_pdf(self, pdf_downloaded: bool) -> PDFData:
        stage_name = ProfileSettingsStagesEnum.STAGE_1_PARSE_PDF
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )
        pdf_data = PDFData()
        if pdf_downloaded:
            pdf_data = PDFParser(self.pdf_download_path).parse()

            logger_msg = "Successfully parsed PDF file"
            self.update_result(stage_result, msg=logger_msg, parsed_data=pdf_data)
            logger.debug(logger_msg)
        else:
            logger_msg = "Error during downloading pdf. Skipping parsing"
            self.update_result(stage_result, msg=logger_msg)
            logger.error(logger_msg)

        self.multi_stage_result.append(stage_result)
        return pdf_data

    def open_my_profile(self) -> None:
        stage_name = ProfileSettingsStagesEnum.STAGE_2_OPEN_MY_PROFILE_SETTINGS
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        try:
            #  Always start from the same time so you can mix stages
            logger.debug("Open main page")
            main_page_link = wait_to_load(self.driver, ps_po.nav_logo_link_selector)
            click_with_move(self.driver, web_element=main_page_link)

            my_profile_link = wait_to_load(self.driver, ms_po.my_settings_link_selector)
            click_with_move(self.driver, web_element=my_profile_link)

            logger_msg = f"Page {self.driver.current_url} successfully opened"
            self.update_result(stage_result, msg=logger_msg)
            logger.debug(logger_msg)

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            self.multi_stage_result.append(stage_result)

    def parse_my_profile(self) -> MyProfile:
        stage_name = ProfileSettingsStagesEnum.STAGE_3_PARSE_MY_PROFILE_SETTINGS
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )
        my_profile_data = MyProfile()
        try:
            my_profile_data = MyProfileParser.parse(self.driver)

            logger_msg = "Successfully parsed My profile page"
            self.update_result(
                stage_result, msg=logger_msg, parsed_data=my_profile_data
            )
            logger.debug(logger_msg)

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            self.multi_stage_result.append(stage_result)

        return my_profile_data

    def open_contact_info(self, user: User) -> None:
        stage_name = ProfileSettingsStagesEnum.STAGE_4_OPEN_CONTACT_INFO_SETTINGS
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )

        try:
            #  Always start from the same time so you can mix stages
            logger.debug("Open main page")
            main_page_link = wait_to_load(self.driver, ps_po.nav_logo_link_selector)
            click_with_move(self.driver, web_element=main_page_link)

            logger.debug("Open My profile page")
            my_profile_link = wait_to_load(self.driver, ms_po.my_settings_link_selector)
            click_with_move(self.driver, web_element=my_profile_link)

            logger.debug("Open Profile settings page")
            profile_settings_link = wait_to_load(
                self.driver, ms_po.profile_settings_link_selector
            )
            click_with_move(self.driver, web_element=profile_settings_link)

            # Possible TFA Stage
            if self.driver.title == "Authorize your device":
                tfa_stage = TFAStage(
                    self.driver,
                    stage_name=ProfileSettingsStagesEnum.ADDITIONAL_STAGE_0_TFA,
                )
                tfa_stage.do_action(user, self.multi_stage_result)

            logger.debug("Open Contact info page")
            contact_info_link = wait_to_load(
                self.driver, ps_po.contact_into_link_selector
            )
            click_with_move(self.driver, web_element=contact_info_link)

            sleep(5)  # seconds
            logger.debug("Click edit account button")
            edit_account_button = wait_to_load(
                self.driver, ci_po.edit_account_button_selector
            )
            click_with_move(self.driver, web_element=edit_account_button)

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            self.multi_stage_result.append(stage_result)

    def parse_contact_info(self) -> ContactInfo:
        stage_name = ProfileSettingsStagesEnum.STAGE_5_PARSE_CONTACT_INFO_SETTINGS
        logger.info(f"Starting stage: {stage_name}")
        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )
        contact_info_data = ContactInfo()
        try:
            contact_info_data = ContactInfoParser.parse(self.driver)

            logger_msg = "Successfully parsed Contact info page"
            self.update_result(
                stage_result, msg=logger_msg, parsed_data=contact_info_data
            )
            logger.debug(logger_msg)

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            self.multi_stage_result.append(stage_result)

        return contact_info_data

    def do_action(self, user: User) -> None:
        logger.info(f"Starting multistage: {self.multi_stage_name}")
        stage_result = self.init_result(
            stage_name=self.multi_stage_name, ip_address=self.ip_address
        )

        download_result = self.download_pdf()  # STAGE 0

        pdf = self.parse_pdf(pdf_downloaded=download_result.status)  # STAGE 1

        self.open_my_profile()  # STAGE 2
        my_profile = self.parse_my_profile()  # STAGE 3

        self.open_contact_info(user)
        contact_info = self.parse_contact_info()

        profile_settings = ProfileSettings(
            account=pdf.user_id,
            employer=my_profile.present_employments,
            created_at=pdf.created_at,
            updated_at=None,
            first_name=pdf.first_name,
            last_name=pdf.last_name,
            full_name=pdf.full_name,
            email=contact_info.email_address,
            phone_number=contact_info.phone_number,
            birth_date=None,
            picture_url=my_profile.profile_picture_url,
            address=contact_info.contact_info_address,
            ssn=None,
            gender=None,
            metadata={},
        )

        logger.info(f"Ending multistage: {self.multi_stage_name} with success")
        self.update_result(
            stage_result,
            msg=f"Successfully ended multistage {self.multi_stage_name}",
            parsed_data=profile_settings,
        )
        self.multi_stage_result.append(stage_result)
