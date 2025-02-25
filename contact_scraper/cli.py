import click
import csv
import sys
import os
from dotenv import load_dotenv
from .scraper import WebScraper

# Load environment variables from .env file
load_dotenv()


@click.command()
@click.argument("url", type=str)
@click.option(
    "--person-type",
    "-t",
    type=str,
    default="all",
    help='Type of person to extract (e.g. "developer", "manager", "support")',
)
@click.option(
    "--contact-methods",
    "-c",
    type=click.Choice(["email", "phone", "all"], case_sensitive=False),
    default="all",
    help="Type of contact information to extract",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="contacts.csv",
    help="Output CSV file path",
)
def main(url: str, person_type: str, contact_methods: str, output: str):
    """
    Extract contact information from a website and save it to a CSV file.

    URL: The website URL to scrape for contact information
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY environment variable not set", err=True)
        sys.exit(1)

    click.echo(f"Scraping contacts from: {url}")
    click.echo(f"Looking for person type: {person_type}")
    click.echo(f"Extracting contact methods: {contact_methods}")

    try:
        scraper = WebScraper(api_key)
        contacts = scraper.scrape_contacts(url, person_type)

        # Filter contacts based on contact_methods
        if contact_methods != "all":
            filtered_contacts = []
            for contact in contacts:
                if contact_methods == "email" and contact.email:
                    filtered_contacts.append(contact)
                elif contact_methods == "phone" and contact.phone:
                    filtered_contacts.append(contact)
            contacts = filtered_contacts

        # Write results to CSV
        with open(output, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=["name", "type", "email", "phone"]
            )
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact.__dict__)

        click.echo(f"Found {len(contacts)} contacts")
        click.echo(f"Results saved to: {output}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
