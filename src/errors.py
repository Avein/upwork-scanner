from selenium.common.exceptions import WebDriverException


class UnknownStageError(WebDriverException):
    """
    Thrown when a driver is in unknown stage.
    """


class TFAStageError(WebDriverException):
    """
    Thrown when a driver is unable to log using Two-factor Authentication.
    """

    pass


class CaptchaError(WebDriverException):
    """
    Thrown when a driver stops on Captcha check.
    """

    pass


class JobFailedException(Exception):
    """
    Thrown when job fail.
    """

    pass
