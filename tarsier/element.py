from pydantic import BaseModel


class Element(BaseModel):
    category: str = ""
    text: str = ""
    text_html: str = ""
    box: list[list[float]] = []
    langs: list[str] = []
    page_number: int = 0
