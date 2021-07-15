from typing import Optional

from bs4 import Tag

from page_objects import Selector


class Parser:
    @staticmethod
    def get_fist_element_text_if_exist(
        element: Tag, selector: Selector
    ) -> Optional[str]:

        result_set = element.select(selector.value)
        if result_set:
            return result_set[0].text
        return None
