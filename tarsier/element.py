from pydantic import BaseModel


class Element(BaseModel):
    category: str = ""
    text: str = ""
    text_html: str = ""
    box: tuple[tuple[float]] = tuple()
    langs: list[str] = []
    page_number: int = 0
