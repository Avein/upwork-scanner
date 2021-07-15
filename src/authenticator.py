import time
from datetime import datetime

import pyotp
from loguru import logger

from credential import backup_user


def get_authenticator_code(
    authenticator_code: str = backup_user.authenticator_secret,
) -> str:

    totp = pyotp.TOTP(authenticator_code)
    time_remaining = totp.interval - datetime.now().timestamp() % totp.interval

    # make sure that code is valid for minimum 5s before returning it
    if time_remaining < 5:
        logger.info("Not enough time to  pass code waiting for new one")
        time.sleep(5)
    return totp.now()
