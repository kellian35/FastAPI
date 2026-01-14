from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    author_id: str