from app.models.article import Article
from app.database.db import db
from bson import ObjectId
from bson.errors import InvalidId
import logging

logger = logging.getLogger(__name__)

async def create_article(article: Article):
    logger.debug(f"Creating article in database: {article.title}")
    try:
        article_dict = article.dict()
        result = await db.articles.insert_one(article_dict)
        created_article = await db.articles.find_one({"_id": result.inserted_id})
        created_article["id"] = str(created_article["_id"])
        del created_article["_id"]
        logger.debug(f"Article created in database: {created_article['id']}")
        return created_article
    except Exception as e:
        logger.error(f"Database error creating article: {str(e)}", exc_info=True)
        raise

async def get_article(article_id: str):
    logger.debug(f"Fetching article from database: {article_id}")
    try:
        article = await db.articles.find_one({"_id": ObjectId(article_id)})
        if article:
            article["id"] = str(article["_id"])
            del article["_id"]
            logger.debug(f"Article found in database: {article_id}")
        else:
            logger.debug(f"Article not found in database: {article_id}")
        return article
    except InvalidId:
        logger.warning(f"Invalid article ID format: {article_id}")
        return None
    except Exception as e:
        logger.error(f"Database error fetching article: {str(e)}", exc_info=True)
        raise

async def get_articles():
    logger.debug("Fetching all articles from database")
    try:
        articles = await db.articles.find().to_list(length=None)
        for article in articles:
            article["id"] = str(article["_id"])
            del article["_id"]
        logger.debug(f"Fetched {len(articles)} articles from database")
        return articles
    except Exception as e:
        logger.error(f"Database error fetching articles: {str(e)}", exc_info=True)
        raise

async def delete_article(article_id: str):
    logger.debug(f"Deleting article from database: {article_id}")
    try:
        result = await db.articles.delete_one({"_id": ObjectId(article_id)})
        if result.deleted_count == 1:
            logger.debug(f"Article deleted from database: {article_id}")
            return True
        else:
            logger.debug(f"Article not found for deletion: {article_id}")
            return False
    except InvalidId:
        logger.warning(f"Invalid article ID format for deletion: {article_id}")
        return False
    except Exception as e:
        logger.error(f"Database error deleting article: {str(e)}", exc_info=True)
        raise