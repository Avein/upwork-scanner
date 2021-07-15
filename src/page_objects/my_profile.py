from selenium.webdriver.common.by import By

from page_objects import Selector

my_settings_link_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-sm-left.p-0-right > div > fe-profile-completeness > div > div.media.m-sm-top > a"
)

employment_list_selector = Selector(
    value="//div[@class='up-card-header']/div/div/h2[contains(.,'Employment history')]/../../../following-sibling::section/div/ul/li",
    type=By.XPATH,
)

profile_image_url_selector = Selector(
    value="section.up-card-section > div.row > div.col > div > div > div > div> div > img.up-avatar"
)

profile_settings_link_selector = Selector(
    value="a[href='/freelancers/settings/profile']"
)
