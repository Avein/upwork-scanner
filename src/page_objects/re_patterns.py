from dataclasses import dataclass


@dataclass
class RePattern:
    value: str
    group_name: str


created_at_pattern = RePattern(
    value="(?<=Active on Upwork Since)\n*(?P<date>.*)\n*", group_name="date"
)

full_name_pattern = RePattern(
    value="(?<=Title)\n*(?P<fullname>.*)", group_name="fullname"
)

user_id_pattern = RePattern(
    value="(?<=Upwork Profile URL)\n*https://www.upwork.com/users/~(?P<user_id>.*)",
    group_name="user_id",
)

address_pattern = RePattern(
    value="(?<=Address)\n*(?P<address>.*)", group_name="address"
)
