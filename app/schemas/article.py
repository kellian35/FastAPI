from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    content: str
    author_id: str

class ArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str