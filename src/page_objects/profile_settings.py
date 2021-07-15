from page_objects import Selector

nav_logo_link_selector = Selector(value="a[href='/home/'].nav-brand")
certificate_of_earnings_url = (
    "https://www.upwork.com/ab/payments/reports/certificate-of-earnings.pdf"
)

report_tab_selector = Selector(
    value="#nav-right > ul > li.nav-dropdown.active > a > span.nav-item-label"
)
certificate_of_earnings = Selector(
    value="#nav-right > ul > li.nav-dropdown.active > ul > li:nth-child(6) > a"
)

contact_into_link_selector = Selector(
    value="body > div:nth-child(8) > div:nth-child(2) > div:nth-child(4) > main:nth-child(1) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(4) > li:nth-child(2) > a:nth-child(1)"
)
