from page_objects import Selector

edit_account_button_selector = Selector(value="button[aria-label='Edit account']")

email_input_selector = Selector(value="input[aria-label='Email']")

address1_span_selector = Selector(value="span[data-test='addressStreet']")
address2_span_selector = Selector(value="span[data-test='addressStreet2']")
city_span_selector = Selector(value="span[data-test='addressCity']")
state_span_selector = Selector(value="span[data-test='addressState']")
zip_span_selector = Selector(value="span[data-test='addressZip']")
country_span_selector = Selector(value="span[data-test='addressCountry']")

phone_span_selector = Selector(value="div[data-test='phone']")


value = (
    "//header[@class='up-card-header']/h2[contains(.,'Location')]/../following-sibling::section.up-card-section/div/ul/li",
)
