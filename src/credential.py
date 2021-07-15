from dataclasses import dataclass

from enums import TFATypeEnum


@dataclass
class User:
    username: str
    password: str
    tfa_type: TFATypeEnum
    secret_answer: str = ""
    authenticator_secret: str = ""

    def __post_init__(self) -> None:
        if self.tfa_type == TFATypeEnum.SECRET and not self.secret_answer:
            raise TypeError(
                "__init__() missing 1 required positional argument:" " 'secret_answer'"
            )

        if self.tfa_type == TFATypeEnum.AUTHENTICATOR and not self.authenticator_secret:
            raise TypeError(
                "__init__() missing 1 required positional argument:"
                " 'authenticator_secret'"
            )


normal_user = User(
    username="bobsuperworker",
    password="Argyleawesome123!",
    secret_answer="number42",
    tfa_type=TFATypeEnum.SECRET,
)

backup_user = User(
    username="bobbybackupy",
    password="Argyleawesome123!",
    secret_answer="number42",
    authenticator_secret="J6PMJ5GNXMGVU47A",
    tfa_type=TFATypeEnum.AUTHENTICATOR,
)
