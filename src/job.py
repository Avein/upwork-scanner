import logging
from typing import List

from loguru import logger
from selenium.common.exceptions import WebDriverException
from tenacity import TryAgain, after_log, retry, stop_after_attempt, wait_exponential

from credential import backup_user
from driver import UpWorkDriver
from errors import CaptchaError, TFAStageError
from stages import StageResult
from stages.job_listing import JobListMultiStage
from stages.login import LoginMultiStage
from stages.profile_settings import ProfileSettingsMultiStage
from utils import save_results


@retry(
    stop=stop_after_attempt(5),
    after=after_log(logger, logging.DEBUG),  # type: ignore
    wait=wait_exponential(multiplier=5, min=4, max=100),
)
def job() -> None:
    # got banned during last test so for now just random ip
    # my_ip = whats_my_ip()
    my_ip = "0.1.2.3"

    with UpWorkDriver(download_path="download") as driver:
        multistage_result: List[StageResult] = list()
        status = "failed"
        try:
            # MULTISTAGE 0
            login_multi_stage = LoginMultiStage(
                driver=driver, multi_stage_result=multistage_result, ip_address=my_ip
            )
            login_multi_stage.do_action(user=backup_user)

            # MULTISTAGE 1
            job_list_multistage = JobListMultiStage(
                driver=driver, multi_stage_result=multistage_result, ip_address=my_ip
            )
            job_list_multistage.do_action()

            # MULTISTAGE 2
            profile_settings_multistage = ProfileSettingsMultiStage(
                driver=driver, multi_stage_result=multistage_result, ip_address=my_ip
            )
            profile_settings_multistage.do_action(user=backup_user)

            status = "success"

        except TFAStageError:
            # TODO ADD POSSIBILITY WITH MULTI TENANT LOGGING eg. [User1, User2]
            logger.info("Try to log with different user")

        except CaptchaError:
            logger.error(
                "Captcha detected change IP or wait before running scanner again"
            )

        except WebDriverException as e:
            logger.error(f"Unexpected error occur: {e}")
            raise TryAgain
        finally:
            save_results(multistage_result, status, driver)


if __name__ == "__main__":
    job()
