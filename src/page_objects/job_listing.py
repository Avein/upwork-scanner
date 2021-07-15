from selenium.webdriver.common.by import By

from page_objects import Selector

submit_job_proposal_button_selector = Selector(
    value="button[aria-label='Submit a Proposal']"
)

jobs_selector = Selector(value="#feed-jobs > section")
load_more_jobs_button_selector = Selector(
    value='//button[contains(.," Load More Jobs ")]', type=By.XPATH
)
# JOB LIST

job_title_selector = Selector(value=".job-title-link")
job_type_selector = Selector(value="[data-job-type] > [data-ng-if]")
job_tier_selector = Selector(value="[data-job-tier] > [data-ng-if]")
job_budget_selector = Selector(value="[data-job-budget] > [data-ng-if]")
job_duration_selector = Selector(value="[data-job-duration] > [data-ng-if]")
job_posted_time_selector = Selector(value="[data-job-posted-time]")
job_description = Selector(value='span[data-ng-bind-html="htmlToTruncate"]')
job_location_requirement_selector = Selector(
    value="[data-job-location-requirement] > [data-ng-if] > span"
)
is_verified_selector = Selector(value=".badge-featured")

skills_required_selector = Selector(value=".skills > span > a")

# PROFILE
categories_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-0-left.p-sm-right > div.m-lg-top.m-sm-left.p-xs-left > fe-fwh-my-categories > div > div > ul > li > a"
)
visibility_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-sm-left.p-0-right > div > fe-profile-completeness > div > div:nth-child(3) > fe-profile-visibility > div > div > div > div > div > div > div.media-body.d-flex > small"
)
availability_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-sm-left.p-0-right > div > fe-profile-completeness > div > div.m-sm-bottom.fe-ui-availability.ng-scope > div > div.media-body.d-flex > small > span"
)
profile_completion_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-sm-left.p-0-right > div > fe-profile-completeness > div > div.row.ng-scope > div > div > div > span > span"
)
available_connections_selector = Selector(
    value="#layout > div.layout-page-content > div > div:nth-child(10) > div.col-md-2.p-sm-left.p-0-right > div > fe-fwh-proposal-stats > div > ul > li > a"
)
