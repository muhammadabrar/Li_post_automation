from playwright.sync_api import sync_playwright
import os
import shutil
import time
from setting import  user_name, password
from db import get_article, update_article
def setup_chrome_profile():
    # Use a persistent profile directory
    profile_dir = os.path.expanduser("~/chrome_automation_profile")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    
    return profile_dir

def main():
    profile_dir = setup_chrome_profile()
    while True:
        pageUrl, postText, article_id = get_article()
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                profile_dir,
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    "--window-size=1920,1080",
                ]
            )
            
            try:
                page = browser.new_page()
                page.goto("https://www.linkedin.com/feed/")
                # Get current page URL
                current_url = page.url
                print(f"Current page URL: {current_url}")
                if "login" in current_url:
                    page.locator('//input[@name="session_key"]').fill(user_name)
                    page.locator('//input[@name="session_password"]').fill(password)
                    # time.sleep(10)
                    page.locator('//button[@type="submit"]').click() 
                    current_url = page.url
                    print(f"Current page URL: {current_url}")
                # Wait for user input before closing
                page.goto(pageUrl)
                create_button = page.locator('//button[.//span[text()= "Create"]]')
                create_button.wait_for(state="visible", timeout=10000)
                create_button.click()
                time.sleep(3)
            
                share_post_button = page.locator('//div[contains(@class, "artdeco-modal__content")]//li[@class= "org-menu__item"]//a[@id="org-menu-POSTS"]')
                share_post_button.wait_for(state="visible", timeout=10000)
                share_post_button.click()
                time.sleep(3)
                # //div[contains(@class, "artdeco-modal__content")]//div[contains(@class, "ql-editor")]
                post_input = page.locator('//div[contains(@class, "artdeco-modal__content")]//div[contains(@class, "ql-editor")]')
                post_input.wait_for(state="visible", timeout=10000)
                post_input.fill(postText)
                time.sleep(3)
                # //button[.//span[text()= "Post"]]
                post_button = page.locator('//button[.//span[text()= "Post"]]')
                post_button.wait_for(state="visible", timeout=10000)
                post_button.click()
                time.sleep(3)
                # Update the article status to published
                update_article(article_id, True)
            finally:
                browser.close()
                time.sleep(30*60)


if __name__ == "__main__":
    main()
