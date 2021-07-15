import re
from dataclasses import dataclass
from typing import Optional

from pdfminer.high_level import extract_text

from page_objects import re_patterns
from page_objects.re_patterns import RePattern


@dataclass
class PDFData:
    user_id: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None
    full_name: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    def __post_init__(self) -> None:
        if self.full_name:
            split = self.full_name.split(" ")
            if len(split) > 1:
                self.last_name = split[-1]
            self.first_name = split[0]


@dataclass
class PDFParser:
    pdf_download_path: str

    def parse_pdf(self, re_pattern: RePattern) -> Optional[str]:
        pdf_text = extract_text(self.pdf_download_path)
        s = re.search(re_pattern.value, pdf_text)
        if s:
            return s.group(re_pattern.group_name)
        return None

    def parse(self) -> PDFData:
        data = PDFData(
            user_id=self.parse_pdf(re_patterns.user_id_pattern),
            address=self.parse_pdf(re_patterns.address_pattern),
            created_at=self.parse_pdf(re_patterns.created_at_pattern),
            full_name=self.parse_pdf(re_patterns.full_name_pattern),
        )
        return data
