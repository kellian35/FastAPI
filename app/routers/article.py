from fastapi import APIRouter, HTTPException, status
from app.schemas.article import ArticleCreate, ArticleResponse
from app.crud.article import create_article, get_article
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Article created successfully"
)
async def create_article_route(article: ArticleCreate):
    logger.info(f"Creating new article: {article.title}")
    try:
        created_article = await create_article(article)
        logger.info(f"Article created successfully: {created_article['id']}")
        return created_article
    except Exception as e:
        logger.error(f"Error creating article: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    response_description="Article details"
)
async def read_article(article_id: str):
    logger.info(f"Fetching article with ID: {article_id}")
    try:
        article = await get_article(article_id)
        if article is None:
            logger.warning(f"Article not found: {article_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        logger.info(f"Article fetched successfully: {article_id}")
        return article
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )