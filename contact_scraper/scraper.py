import requests
import html2text
from typing import Optional, List
from .agent import ContactAgent, Contact


class WebScraper:
    def __init__(self, api_key: str):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.agent = ContactAgent(api_key)

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch webpage and convert to markdown"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            html_content = response.text
            markdown_content = self.html_converter.handle(html_content)

            return markdown_content
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch webpage: {str(e)}")

    def scrape_contacts(self, url: str, person_type: str) -> List[Contact]:
        """Scrape contacts from the website"""
        contacts = []
        visited_urls = set()

        # Get initial page
        markdown_content = self.fetch_page(url)
        if not markdown_content:
            return contacts

        # Find potential contact pages
        contact_urls = self.agent.find_contact_pages(markdown_content, url)
        contact_urls.insert(0, url)  # Also check the initial page

        # Visit each page and extract contacts
        for page_url in contact_urls:
            if page_url in visited_urls:
                continue

            visited_urls.add(page_url)
            try:
                page_content = self.fetch_page(page_url)
                if page_content:
                    page_contacts = self.agent.extract_contacts(
                        page_content, person_type
                    )
                    contacts.extend(page_contacts)
            except Exception as e:
                print(f"Error processing {page_url}: {str(e)}")

        return contacts
