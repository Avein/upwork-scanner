# Login Page
from page_objects import Selector

login_page_url = "https://www.upwork.com/ab/account-security/login"

username_input_selector = Selector(value="#login_username")
username_button_selector = Selector(value="#login_password_continue")

# Login page stage 2
password_input_selector = Selector(value="#login_password")
password_button_selector = Selector(value="#login_control_continue")

# Main page
jobs_list_selector = Selector(value="#feed-jobs")

# Secret page
secret_question_input_selector = Selector(value="#deviceAuth_answer")
secret_question_button_selector = Selector(value="#control_save")

# Authenticator page
authenticator_input_selector = Selector(value="#deviceAuthOtp_otp")
authenticator_button_selector = Selector(value="#next_continue")

# Profile settings page
profile_page_selector = Selector(
    value="#main > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div.up-card.py-0.d-none.d-lg-block"
)

# Banned page
captcha_selector = Selector(value="body > section > div.page-title-wrapper > div > h1")
