from pymongo import MongoClient
from setting import mongo_url


# Connect to MongoDB
client = MongoClient(mongo_url)
db = client.SCRAP
collection = db.article

def get_article():
    pageUrl = "https://www.linkedin.com/company/mako-technic/"
    postText = "Welcome to Mako Technic"
    article = collection.find_one({"isPublished_Li": False}, {"Li_post_content": 1, "Li_page_url": 1})
    if article:
        pageUrl = article.get("Li_page_url", pageUrl) # Use provided URL as fallback
        postText = article.get("Li_post_content", postText) # Use provided text as fallback
        article_id = article.get("_id")
    return pageUrl, postText, article_id

if __name__ == "__main__":
    pageUrl, postText, article_id = get_article()
    print(pageUrl, postText, article_id)

def update_article(article_id, isPublished_Li):
    collection.update_one({"_id": article_id}, {"$set": {"isPublished_Li": isPublished_Li}})

