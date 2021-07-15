from enum import Enum
from typing import Union


class TFATypeEnum(Enum):
    SECRET = "Secret Question"
    AUTHENTICATOR = "Authenticator"
    NONE = "None"


class LoginStagesEnum(Enum):
    STAGE_0_OPEN_PAGE = "Stage 0: Open page"
    STAGE_1_USERNAME = "Stage 1: Username stage"
    STAGE_2_PASSWORD = "Stage 2: Password stage"
    STAGE_3_TFA = "Stage 3: TFA stage"
    MULTISTAGE_0_LOGIN = "Multistage 0: Login"


class JobListStagesEnum(Enum):
    STAGE_0_LOAD_JOBS_LIST = "Stage 0: Load jobs list"
    STAGE_1_SCRAPE_JOBS_LIST = "Stage 1: Scrape jobs list"
    STAGE_2_SCRAPE_PROFILE = "Stage 2: Scrape profile"
    MULTISTAGE_1_JOB_LIST = "Multistage: 1: Job list page scraping"


class ProfileSettingsStagesEnum(Enum):
    ADDITIONAL_STAGE_0_TFA = "Additional Stage 0: TFA stage"

    STAGE_0_DOWNLOAD_CERTIFICATE_PDF = "Stage 0: Download certificate of earnings pdf"
    STAGE_1_PARSE_PDF = "Stage 1: Parse certificate of earnings pdf"

    STAGE_2_OPEN_MY_PROFILE_SETTINGS = "Stage 2: Open My profile settings"
    STAGE_3_PARSE_MY_PROFILE_SETTINGS = "Stage 3: Parse My profile settings"

    STAGE_4_OPEN_CONTACT_INFO_SETTINGS = "Stage 4: Open Contact info settings"
    STAGE_5_PARSE_CONTACT_INFO_SETTINGS = "Stage 5: Parse Contact info settings"

    MULTISTAGE_2_PROFILE_SETTINGS = "Multistage: 2: Profile settings page scraping"


TFA_STAGE_ENUMS = Union[LoginStagesEnum, ProfileSettingsStagesEnum]
