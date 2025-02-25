from typing import List, Optional
import openai
from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str = Field(..., description="The full name of the contact")
    type: str = Field(..., description="The role or type of the contact")
    email: Optional[str] = Field(None, description="Email address of the contact")
    phone: Optional[str] = Field(None, description="Phone number of the contact")


class ContactList(BaseModel):
    contacts: List[Contact] = Field(..., description="A list of contacts")


class ContactAgent:
    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)

    def find_contact_pages(self, markdown_content: str, base_url: str) -> List[str]:
        """Suggests pages that might contain contact information"""
        prompt = f"""
        Given this webpage content, identify URLs that might contain contact information.
        Focus on links containing words like 'contact', 'about', 'team', 'people', etc.
        Only return URLs, one per line. If a URL is relative, use the base URL: {base_url}
        
        Webpage content:
        {markdown_content[:2000]}  # Limit content length for token constraints
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Using 4o mini model
            messages=[
                {
                    "role": "system",
                    "content": """You are a web crawler focused on finding contact information pages.
                    Return only valid URLs, one per line. No additional text or explanations.""",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        urls = response.choices[0].message.content.strip().split("\n")
        return [url.strip() for url in urls if url.strip()]

    def extract_contacts(
        self, markdown_content: str, person_type: str
    ) -> List[Contact]:
        """Extracts contact information for specified person type"""
        prompt = f"""
        Extract contact information from this webpage content.
        Look for people who match the type: {person_type}

        Requirements:
        1. Only include people that match the specified type
        2. Extract name, type/role, email, and phone
        3. Return in JSON format compatible with this Pydantic model:

        class Contact(BaseModel):
            name: str  # Full name of the contact
            type: str  # Role or type of the contact
            email: Optional[str] = None  # Email address if available
            phone: Optional[str] = None  # Phone number if available

        Webpage content:
        {markdown_content[:3000]}
        """

        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Using 4o mini model
            messages=[
                {
                    "role": "system",
                    "content": """You are a contact information extraction specialist.
                    Return data in a JSON array format that matches the specified Pydantic model.""",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format=ContactList,
        )

        try:
            data = response.choices[0].message.parsed
            return data.contacts

        except Exception as e:
            print(f"Error processing response: {str(e)}")
            return []
