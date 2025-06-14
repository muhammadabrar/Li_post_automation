from pymongo import MongoClient
from setting import mongo_url
from bson import ObjectId


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



def update_article(article_id, isPublished_Li):
    try:
        # Return the updated document instead of the original one
        result = collection.find_one_and_update(
            {"_id": ObjectId(article_id)},
            {"$set": {"isPublished_Li": isPublished_Li}},
            return_document=True  # This makes it return the updated document
        )
        if result is None:
            print(f"No article found with ID: {article_id}")
            return False
        print(f"Successfully updated article: {result}")
        return True
    except Exception as e:
        print(f"Error updating article: {str(e)}")
        return False


if __name__ == "__main__":
    # pageUrl, postText, article_id = get_article()
    # print(pageUrl, postText, article_id)
    update_article("684d176411564d3422af8f35", True)
