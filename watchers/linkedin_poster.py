#!/usr/bin/env python3
"""
LinkedIn Poster for AI Employee
Automatically posts content to LinkedIn using Playwright browser automation.
"""
import asyncio
import logging
import json
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
READY_TO_POST_PATH = VAULT_PATH / "Ready_To_Post" / "LinkedIn"
DONE_PATH = VAULT_PATH / "Done"
ACCOUNTING_PATH = VAULT_PATH / "Accounting"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / "linkedin_poster.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('LinkedInPoster')


class LinkedInPoster:
    """LinkedIn Poster for automated posting via browser automation."""

    def __init__(self):
        """Initialize LinkedIn Poster."""
        self.ready_to_post = READY_TO_POST_PATH
        self.ready_to_post.mkdir(parents=True, exist_ok=True)
        self.done_path = DONE_PATH
        self.accounting_path = ACCOUNTING_PATH
        self.accounting_path.mkdir(parents=True, exist_ok=True)

    def parse_post_file(self, post_file: Path) -> dict:
        """
        Parse LinkedIn post file to extract content.

        Args:
            post_file: Path to post markdown file

        Returns:
            Dictionary with post content and metadata
        """
        try:
            content = post_file.read_text(encoding='utf-8')

            # Extract metadata
            metadata = {}
            in_frontmatter = False
            frontmatter_lines = []

            for line in content.split('\n'):
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                        continue
                    else:
                        break
                if in_frontmatter:
                    frontmatter_lines.append(line)

            for line in frontmatter_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            # Extract post content (after second ---)
            parts = content.split('---', 2)
            if len(parts) > 2:
                post_content = parts[2].strip()
            else:
                post_content = content

            return {
                'metadata': metadata,
                'content': post_content,
                'file_path': post_file
            }

        except Exception as e:
            logger.error(f"Error parsing post file {post_file}: {e}")
            return None

    async def post_to_linkedin(self, content: str, post_file: Path = None) -> bool:
        """
        Post content to LinkedIn using Playwright.

        Args:
            content: Post content to publish
            post_file: Original post file path (for logging)

        Returns:
            True if successful
        """
        try:
            logger.info("Starting LinkedIn posting automation...")

            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                # Navigate to LinkedIn
                logger.info("Navigating to LinkedIn...")
                await page.goto('https://www.linkedin.com/login')
                await page.wait_for_load_state('networkidle')

                # Check if already logged in or need to login
                if 'login' in page.url:
                    logger.info("Login required - please log in manually")
                    logger.info("Waiting for login...")

                    # Wait for user to login manually (up to 5 minutes)
                    await page.wait_for_url('feed/', timeout=300000)
                    logger.info("Login successful!")

                # Navigate to start a post
                logger.info("Navigating to create post...")
                await page.goto('https://www.linkedin.com/feed/')
                await page.wait_for_load_state('networkidle')

                # Click "Start a post" button
                try:
                    # Try multiple selectors for the post button
                    post_button_selectors = [
                        'button[aria-label="Start a post"]',
                        'button[data-control-name="create_post"]',
                        'span:has-text("Start a post")',
                        'div.share-box-feed-entry__trigger button'
                    ]

                    post_button = None
                    for selector in post_button_selectors:
                        try:
                            post_button = await page.wait_for_selector(selector, timeout=5000)
                            if post_button:
                                break
                        except:
                            continue

                    if post_button:
                        await post_button.click()
                        await page.wait_for_timeout(2000)
                    else:
                        logger.error("Could not find 'Start a post' button")
                        return False

                except Exception as e:
                    logger.error(f"Error clicking post button: {e}")
                    return False

                # Wait for text editor to appear
                logger.info("Waiting for text editor...")
                await page.wait_for_timeout(2000)

                # Find text area and type content
                text_area_selectors = [
                    'div[contenteditable="true"][role="textbox"]',
                    'div[data-test-urn="post-text-area"]',
                    'div[data-control-name="post-content"]',
                    'textarea[name="post-text"]'
                ]

                text_area = None
                for selector in text_area_selectors:
                    try:
                        text_area = await page.wait_for_selector(selector, timeout=5000)
                        if text_area:
                            break
                    except:
                        continue

                if text_area:
                    # Click on text area to focus
                    await text_area.click()
                    await page.wait_for_timeout(500)

                    # Type the content
                    await text_area.type(content, delay=10)
                    logger.info("Content typed into LinkedIn post editor")
                else:
                    logger.error("Could not find text editor")
                    return False

                # Wait a bit to see if post appeared
                await page.wait_for_timeout(3000)

                # Look for post button and click it
                logger.info("Looking for post button...")

                post_button_selectors = [
                    'button[aria-label="Post"]',
                    'button[data-control-name="submit_post"]',
                    'button:has-text("Post")',
                    'div.share-actions button:has-text("Post")'
                ]

                submit_button = None
                for selector in post_button_selectors:
                    try:
                        submit_button = await page.wait_for_selector(selector, timeout=5000)
                        if submit_button:
                            break
                    except:
                        continue

                if submit_button:
                    await submit_button.click()
                    logger.info("Post button clicked!")
                    await page.wait_for_timeout(5000)
                else:
                    logger.warning("Could not find Post button - you may need to click manually")

                # Take screenshot for verification
                screenshot_path = VAULT_PATH / f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                await page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")

                # Keep browser open for verification
                logger.info("Browser will stay open for 30 seconds for verification...")
                logger.info("You can cancel the post if something is wrong")
                await page.wait_for_timeout(30000)

                await browser.close()
                return True

        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False

    async def check_queue(self) -> list:
        """
        Check Ready_To_Post/LinkedIn/ folder and process pending posts.

        Returns:
            List of processed posts
        """
        try:
            if not self.ready_to_post.exists():
                logger.info("No Ready_To_Post/LinkedIn/ folder")
                return []

            post_files = list(self.ready_to_post.glob("*.md"))

            if not post_files:
                logger.info("No LinkedIn posts ready")
                return []

            logger.info(f"Found {len(post_files)} LinkedIn posts to process")
            processed = []

            for post_file in post_files:
                try:
                    # Parse post file
                    post_data = self.parse_post_file(post_file)
                    if not post_data:
                        continue

                    content = post_data['content']

                    # Post to LinkedIn
                    logger.info(f"Posting: {post_file.name}")
                    success = await self.post_to_linkedin(content, post_file)

                    if success:
                        # Move to Done
                        done_filename = f"{datetime.now().strftime('%Y-%m-%d')}_posted_linkedin_{post_file.name}"
                        done_path = self.done_path / done_filename
                        post_file.rename(done_path)

                        # Log to accounting
                        self._log_post_activity(post_data, done_filename)

                        processed.append({
                            'original': str(post_file.name),
                            'done_file': str(done_filename),
                            'status': 'posted'
                        })

                        logger.info(f"Successfully posted and archived: {post_file.name}")

                except Exception as e:
                    logger.error(f"Error processing {post_file.name}: {e}")

            return processed

        except Exception as e:
            logger.error(f"Error checking queue: {e}")
            return []

    def _log_post_activity(self, post_data: dict, done_filename: str):
        """Log post activity to accounting file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m")
            metrics_file = self.accounting_path / f"LinkedIn_Metrics_{timestamp}.md"

            # Append to metrics file
            with open(metrics_file, 'a') as f:
                f.write(f"\n## Posted: {done_filename}\n")
                f.write(f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"- **File:** {done_filename}\n")
                f.write(f"- **Status:** Posted\n")
                f.write("\n")

        except Exception as e:
            logger.error(f"Error logging post activity: {e}")


async def main():
    """Main entry point for LinkedIn Poster."""
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Poster for AI Employee')
    parser.add_argument('--post', type=str, help='Post content directly')
    parser.add_argument('--check-queue', action='store_true',
                       help='Check Ready_To_Post/LinkedIn/ and post pending content')
    parser.add_argument('--list', action='store_true',
                       help='List pending posts')

    args = parser.parse_args()

    poster = LinkedInPoster()

    if args.post:
        # Post content directly
        logger.info("Posting content to LinkedIn...")
        success = await poster.post_to_linkedin(args.post)
        if success:
            logger.info("Post successful!")
        else:
            logger.error("Post failed")

    elif args.check_queue:
        # Check queue and post pending items
        logger.info("Checking LinkedIn post queue...")
        processed = await poster.check_queue()
        logger.info(f"Processed {len(processed)} posts")

    elif args.list:
        # List pending posts
        if poster.ready_to_post.exists():
            posts = list(poster.ready_to_post.glob("*.md"))
            logger.info(f"Found {len(posts)} pending LinkedIn posts:")
            for post in posts:
                logger.info(f"  - {post.name}")
        else:
            logger.info("No Ready_To_Post/LinkedIn/ folder")

    else:
        logger.info("No action specified. Use --check-queue, --list, or --post")


if __name__ == "__main__":
    asyncio.run(main())
