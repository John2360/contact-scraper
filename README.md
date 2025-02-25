# Contact Scraper

A command-line tool that extracts contact information from websites. It uses AI to identify and extract contact details for specific types of people (e.g., developers, managers, support staff).

## Features

- Extract contact information including names, emails, and phone numbers
- Filter contacts by role/type (e.g., "developer", "manager")
- Filter by contact method (email or phone)
- Export results to CSV
- Intelligent page navigation to find contact information
- AI-powered contact extraction

## Installation

1. Make sure you have Python 3.12+ and [Poetry](https://python-poetry.org/) installed.

2. Clone the repository:

```bash
git clone https://github.com/yourusername/contact-scraper.git
cd contact-scraper
```

3. Install dependencies:

```bash
poetry install
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key
```

## Usage

```bash
poetry run contact-scraper <url> [options]
```

### Options

- `-t, --person-type`: Type of person to extract (e.g., "developer", "manager")
- `-c, --contact-methods`: Contact methods to extract (e.g., "email", "phone")
- `-o, --output`: Output file path (default: "contacts.csv")

### Example

```bash
poetry run contact-scraper https://example.com -t developer -c email -o contacts.csv
```

This will extract all contacts of type "developer" and save the results to `contacts.csv`.

## Output Format

The tool generates a CSV file with the following columns:

- name: Full name of the contact
- type: Role or type of the person
- email: Email address (if found)
- phone: Phone number (if found)

## Requirements

- Python 3.12+
- OpenAI API key
- Poetry for dependency management

## License

MIT License
