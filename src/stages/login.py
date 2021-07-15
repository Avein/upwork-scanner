from dataclasses import dataclass, field
from typing import List, Optional, Type, Union

from loguru import logger
from selenium.common.exceptions import TimeoutException

from authenticator import get_authenticator_code
from config import TimeoutsEnum
from credential import User
from enums import TFA_STAGE_ENUMS, LoginStagesEnum, TFATypeEnum
from errors import TFAStageError
from helpers import click_with_move, find_element_by, send_keys_with_delay, wait_to_load
from page_objects import Selector
from page_objects import job_listing as jl_po
from page_objects import login as po
from stages import Stage, StageResult


@dataclass
class UsernameStage(Stage):
    selector: Selector = po.username_input_selector
    stage_name: LoginStagesEnum = LoginStagesEnum.STAGE_1_USERNAME

    def do_action(self, user: User, multi_stage_results: list) -> None:
        logger.info(f"Starting stage: {self.stage_name}")
        stage_result = self.init_result(
            stage_name=self.stage_name, ip_address=self.ip_address
        )

        try:
            logger.debug(f"Logging with user: {user.username}")
            username_input_field = wait_to_load(self.driver, po.username_input_selector)
            send_keys_with_delay(web_element=username_input_field, text=user.username)

            login_button = find_element_by(self.driver, po.username_button_selector)
            click_with_move(self.driver, web_element=login_button)

            logger.info(f"Ending stage: {self.stage_name} with success")
            self.update_result(stage_result, msg="Successfully sent username into form")

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            multi_stage_results.append(stage_result)


@dataclass
class PasswordStage(Stage):
    selector: Selector = po.password_input_selector
    stage_name: LoginStagesEnum = LoginStagesEnum.STAGE_2_PASSWORD

    def do_action(self, user: User, multi_stage_results: list) -> None:
        logger.info(f"Starting stage: {self.stage_name}")
        stage_result = self.init_result(
            stage_name=self.stage_name, ip_address=self.ip_address
        )

        try:
            logger.debug("Sending password")
            password_input_field = wait_to_load(self.driver, po.password_input_selector)
            send_keys_with_delay(web_element=password_input_field, text=user.password)

            password_button = find_element_by(self.driver, po.password_button_selector)
            click_with_move(self.driver, web_element=password_button)

            logger.info(f"Ending stage: {self.stage_name} with success")
            self.update_result(stage_result, msg="Successfully sent password into form")

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            multi_stage_results.append(stage_result)


@dataclass
class SecretAnswerStage(Stage):
    selector: Selector = po.secret_question_input_selector
    tfa_type: TFATypeEnum = TFATypeEnum.SECRET

    def do_action(self, user: User) -> None:
        logger.info(f"Starting stage TFA type: {self.tfa_type}")
        logger.debug("Filling secret answer form")
        secret_question_input_field = wait_to_load(
            self.driver, po.secret_question_input_selector
        )
        send_keys_with_delay(
            web_element=secret_question_input_field, text=user.secret_answer
        )

        secret_question_button = find_element_by(
            self.driver, po.secret_question_button_selector
        )
        click_with_move(self.driver, web_element=secret_question_button)
        logger.info(f"Ending stage 3 TFA type: {self.tfa_type}")


@dataclass
class AuthenticatorStage(Stage):
    selector: Selector = po.authenticator_input_selector
    tfa_type: TFATypeEnum = TFATypeEnum.AUTHENTICATOR

    def do_action(self, user: User) -> None:
        logger.info(f"Starting stage TFA type: {self.tfa_type}")
        logger.debug("Getting authenticator code")
        authenticator_code = get_authenticator_code(user.authenticator_secret)
        logger.debug("Filling authenticator code form")

        authenticator_input_field = wait_to_load(
            self.driver, po.authenticator_input_selector
        )
        send_keys_with_delay(
            web_element=authenticator_input_field, text=authenticator_code
        )

        authenticator_button = find_element_by(
            self.driver, po.authenticator_button_selector
        )
        click_with_move(self.driver, web_element=authenticator_button)
        logger.info(f"Ending stage 3 TFA type: {self.tfa_type}")


@dataclass
class TFAStage(Stage):
    selector: Optional[Selector] = None
    stage_name: TFA_STAGE_ENUMS = LoginStagesEnum.STAGE_3_TFA

    TFA_STAGE_TYPE = Union[AuthenticatorStage, SecretAnswerStage]

    def define_stage(
        self, possible_stages: List[Type[TFA_STAGE_TYPE]]
    ) -> TFA_STAGE_TYPE:
        for stage in possible_stages:
            try:
                stage_object = stage(self.driver)
                wait_to_load(
                    stage_object.driver,
                    selector=stage_object.selector,
                    timeout=TimeoutsEnum.MEDIUM,
                )
                return stage_object
            except TimeoutException:
                continue
        else:
            raise TimeoutException(msg="Can not define stage")

    def do_action(self, user: User, multi_stage_results: list) -> None:
        logger.info(f"Starting stage: {self.stage_name}")
        stage_result = self.init_result(
            stage_name=self.stage_name, ip_address=self.ip_address
        )

        logger.debug("Trying to define TFA type")
        try:
            tfa_type_stage = self.define_stage([AuthenticatorStage, SecretAnswerStage])
            logger.debug(
                f"Type defined: {tfa_type_stage.tfa_type}. "
                f"Checking if user is able to log with given TFA type"
            )

            if user.tfa_type == tfa_type_stage.tfa_type:
                tfa_type_stage.do_action(user)
                logger.info(f"Ending stage: {self.stage_name} with success")
                self.update_result(
                    stage_result,
                    msg=f"Successfully logged with user: {user.username} "
                    f"using {tfa_type_stage.tfa_type} TFA type",
                )
            else:
                logger_msg = (
                    f"User is unable to log with {tfa_type_stage.tfa_type} TFA type"
                )
                logger.error(logger_msg)
                self.update_result(
                    stage_result,
                    result_status=False,
                    msg=logger_msg,
                    error=TFAStageError,
                )
                raise TFAStageError(msg=logger_msg)

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            multi_stage_results.append(stage_result)


@dataclass
class LoginMultiStage(Stage):

    selector: Optional[Selector] = None
    multi_stage_result: List[StageResult] = field(default_factory=lambda: list())
    multi_stage_name: LoginStagesEnum = LoginStagesEnum.MULTISTAGE_0_LOGIN

    def open_login_page(self, url: str = po.login_page_url) -> None:
        stage_name = LoginStagesEnum.STAGE_0_OPEN_PAGE
        logger.info(f"Starting stage: {stage_name}")

        stage_result = self.init_result(
            stage_name=stage_name, ip_address=self.ip_address
        )
        try:
            logger.debug(f"Opening page {url}")
            self.driver.get(url)
            wait_to_load(
                self.driver, po.username_input_selector, timeout=TimeoutsEnum.SMALL
            )
            self.update_result(stage_result, msg=f"Successfully opened page {url}")

        except TimeoutException:
            logger.error("Could not open page checking possible captcha")
            self.check_captcha(result=stage_result)

        finally:
            self.multi_stage_result.append(stage_result)

    def do_action(self, user: User) -> None:
        logger.info(f"Starting multistage: {self.multi_stage_name}")
        stage_result = self.init_result(
            stage_name=self.multi_stage_name, ip_address=self.ip_address
        )

        self.open_login_page()  # STAGE 0

        username_stage = UsernameStage(self.driver)  # STAGE 1
        username_stage.do_action(user, self.multi_stage_result)

        password_stage = PasswordStage(self.driver)  # STAGE 2
        password_stage.do_action(user, self.multi_stage_result)

        # Sometimes TFA stage is not needed
        if not self.is_logged():
            tfa_stage = TFAStage(self.driver)  # STAGE 3
            tfa_stage.do_action(user, self.multi_stage_result)

        if not self.is_logged():  # MULTISTAGE 0
            self.check_captcha(stage_result)

        logger.info(f"Ending multistage: {self.multi_stage_name} with success")
        self.update_result(stage_result, msg="User successfully logged in")
        self.multi_stage_result.append(stage_result)

    def is_logged(self) -> bool:
        try:
            wait_to_load(self.driver, selector=jl_po.load_more_jobs_button_selector)
            return True
        except TimeoutException:
            return False
