import requests
import pandas as pd
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FacultyScrapingInput(BaseModel):
    url: str = Field(description="The URL to scrape faculty data from")
    output_file: str = Field(default="faculty_profiles.csv", description="Output CSV file name")

class FacultyScrapingTool(BaseTool):
    name: str = "scrape_faculty_data"
    description: str = "Scrapes faculty data from university website and saves to CSV"
    args_schema: Type[BaseModel] = FacultyScrapingInput

    def _run(self, url: str, output_file: str = "faculty_profiles.csv") -> str:
        """Scrape faculty data from UOW website and save to CSV file."""
        print("🔍 Starting faculty data scraping...")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            data = []
            faculty_blocks = soup.find_all("div", class_="event-details")

            print(f"📊 Found {len(faculty_blocks)} faculty blocks")

            for block in faculty_blocks:
                name_tag = block.find("h2")
                name = name_tag.get_text(strip=True) if name_tag else "Unknown"
                dep = "Computer Science"

                qualification = research_interests = tel = email = None
                p_tag = block.find("p")
                if p_tag:
                    for b in p_tag.find_all("b"):
                        label = b.get_text(strip=True)
                        if "Qualification" in label:
                            qualification = b.next_sibling.strip() if b.next_sibling else None
                        elif "Research Interests" in label:
                            research_interests = b.next_sibling.strip() if b.next_sibling else None
                        elif "Tel" in label:
                            tel = b.next_sibling.strip() if b.next_sibling else None
                        elif "Email" in label:
                            email_tag = b.find_next("a", href=lambda h: h and "mailto:" in h)
                            email = email_tag.get_text(strip=True) if email_tag else None

                data.append({
                    "Name": name,
                    "Department": dep,
                    "Qualification": qualification or "Not specified",
                    "Research Interests": research_interests or "Not specified",
                    "Tel": tel or "Not provided",
                    "Email": email or "Not provided"
                })

            df = pd.DataFrame(data)
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print(f"✅ Successfully scraped {len(data)} faculty profiles")
            print(f"💾 Data saved to {output_file}")
            return f"Successfully scraped {len(data)} faculty profiles and saved to {output_file}"

        except Exception as e:
            error_msg = f"Error scraping data: {e}"
            print(f"❌ {error_msg}")
            return error_msg

    def _arun(self, url: str, output_file: str = "faculty_profiles.csv") -> str:
        raise NotImplementedError("Async not implemented")
