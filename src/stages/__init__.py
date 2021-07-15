from dataclasses import dataclass
from typing import Optional, Sequence, Type, Union

from loguru import logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from undetected_chromedriver import Chrome

from config import TimeoutsEnum
from enums import (
    JobListStagesEnum,
    LoginStagesEnum,
    ProfileSettingsStagesEnum,
    TFATypeEnum,
)
from errors import CaptchaError, UnknownStageError
from helpers import wait_to_load
from models.job_listing import Job, PersonalData, Profile
from models.profile_settings import ProfileSettings
from page_objects import login as po
from page_objects.login import Selector
from parsers.certificate_of_earnings_pdf import PDFData
from parsers.contact_info import ContactInfo
from parsers.my_profile import MyProfile

STAGE_NAME_ENUMS = Union[LoginStagesEnum, JobListStagesEnum, ProfileSettingsStagesEnum]
PARSED_DATA = Union[
    Job, Profile, PersonalData, PDFData, MyProfile, ContactInfo, ProfileSettings
]


@dataclass
class StageResultData:
    msg: Optional[str] = None
    error: Optional[Type[WebDriverException]] = None
    parsed_data: Optional[PARSED_DATA] = None
    parsed_data_list: Optional[Sequence[PARSED_DATA]] = None


@dataclass
class StageResult:
    status: bool
    data: StageResultData
    name: Optional[STAGE_NAME_ENUMS] = None
    ip: Optional[str] = None


@dataclass
class Stage:
    driver: Chrome
    selector: Optional[Selector] = None
    result: Optional[StageResult] = None
    tfa_type: TFATypeEnum = TFATypeEnum.NONE
    ip_address: Optional[str] = None

    @staticmethod
    def init_result(
        stage_name: STAGE_NAME_ENUMS, ip_address: Optional[str]
    ) -> StageResult:
        ip = ip_address
        data = StageResultData()
        result = StageResult(status=True, data=data, name=stage_name, ip=ip)

        return result

    @staticmethod
    def update_result(
        result: StageResult,
        result_status: bool = True,
        msg: Optional[str] = None,
        error: Optional[Type[WebDriverException]] = None,
        parsed_data: Optional[PARSED_DATA] = None,
        parsed_data_list: Optional[Sequence[PARSED_DATA]] = None,
    ) -> StageResult:
        if not result_status:
            result.status = result_status
        if msg:
            result.data.msg = msg
        if error:
            result.data.error = error
        if parsed_data:
            result.data.parsed_data = parsed_data
        if parsed_data_list:
            result.data.parsed_data_list = parsed_data_list

        return result

    def check_captcha(self, result: StageResult) -> None:
        is_captcha = Captcha(self.driver).check_captcha()
        if is_captcha:
            logger_msg = f"Captcha found terminating on stage {result.name}"
            logger.error(logger_msg)
            self.update_result(
                result, result_status=False, error=CaptchaError, msg="Captcha ban"
            )
            raise CaptchaError(msg=logger_msg)
        else:
            logger_msg = f"Unknown error occur on page with title: {self.driver.title}"
            logger.error(logger_msg)
            self.update_result(
                result, result_status=False, error=UnknownStageError, msg=logger_msg
            )
            raise UnknownStageError(msg=logger_msg)


@dataclass
class Captcha:
    driver: Chrome
    selector: Selector = po.captcha_selector

    def check_captcha(self) -> bool:
        try:
            element = wait_to_load(
                self.driver, selector=self.selector, timeout=TimeoutsEnum.SMALL
            )

            if element.text == "Please verify you are a human":
                logger.error("Captcha found")
                return True
            else:
                return False
        except TimeoutException:

            logger.debug("No captcha found")
            return False
