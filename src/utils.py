import dataclasses
import json
import os
import pickle
from datetime import datetime
from enum import Enum
from typing import Any, List

from Screenshot import Screenshot_Clipping
from selenium.common.exceptions import WebDriverException
from undetected_chromedriver import Chrome

from stages import StageResult

base_path = os.getcwd()


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, type(WebDriverException)):
            return str(o)

        return super().default(o)


def save_results(
    multistage_result: List[StageResult], status: str, driver: Chrome
) -> None:
    # find last run
    results_path = os.path.join(base_path, "results")
    list_dir = sorted(
        [
            name
            for name in os.listdir(results_path)
            if os.path.isdir(os.path.join(results_path, name))
        ],
        key=lambda x: float(x.split("-")[0]),
    )

    # define folder name
    if list_dir:
        last_run_id = int(list_dir[-1].split("-")[0]) + 1
    else:
        last_run_id = 0

    date = datetime.now().strftime("%m.%d.%Y-%H:%M:%S")

    folder_name = f"{last_run_id}-{status}-{date}"
    folder_path = os.path.join(base_path, "results", folder_name)
    os.mkdir(folder_path)

    # save res
    pickle.dump(
        multistage_result,
        open(os.path.join(folder_path, "multi_stage_results.res"), "wb"),
    )

    # save json
    with open(
        os.path.join(folder_path, "multi_stage_results.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(
            multistage_result, f, ensure_ascii=False, indent=4, cls=EnhancedJSONEncoder
        )

    # if failed save additional data: screenshot and page source
    # which can help with debugging errors
    if status == "failed":
        page_source = driver.page_source  # type: ignore
        with open(os.path.join(folder_path, "multi_stage_results.html"), "w") as f:
            f.write(page_source)

        ob = Screenshot_Clipping.Screenshot()
        ob.full_Screenshot(driver, save_path=folder_path, image_name="screenshot.png")
