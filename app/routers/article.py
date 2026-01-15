from fastapi import APIRouter, HTTPException, status
from app.schemas.article import ArticleCreate, ArticleResponse
from app.crud.article import create_article, get_article, get_articles, delete_article
from app.crud.user import get_user
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
        user = await get_user(article.author_id)
        if not user:
            logger.warning(
                f"Attempt to create article with non-existent user: {article.author_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist"
            )

        created_article = await create_article(article)
        logger.info(f"Article created successfully")
        return created_article

    except HTTPException:
        raise

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

@router.get(
    "/",
    response_model=list[ArticleResponse],
    response_description="List of all articles")
async def read_articles():
    logger.info("Fetching all articles")
    try:
        articles = await get_articles()
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Article deleted successfully"
)
async def delete_article_route(article_id: str):
    logger.info(f"Deleting article with ID: {article_id}")
    try:
        deleted = await delete_article(article_id)
        if not deleted:
            logger.warning(f"Article not found for deletion: {article_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        logger.info(f"Article deleted successfully: {article_id}")
    except Exception as e:
        logger.error(f"Error deleting article: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )