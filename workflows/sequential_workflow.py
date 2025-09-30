from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from tools.faculty_scraper import FacultyScrapingTool
from tools.email_campaign import EmailCampaignTool
from llm_setup import llm
from config import test_recipient

class SequentialEmailWorkflow:
    def __init__(self):
        self.scraping_prompt = PromptTemplate(
            input_variables=["url"],
            template="Scrape faculty data from this URL: {url}. Save the data to CSV format."
        )

        self.email_prompt = PromptTemplate(
            input_variables=["faculty_data", "test_email"],
            template="Generate and send personalized emails to faculty members. Faculty data: {faculty_data}. Send all emails to test inbox: {test_email}"
        )

        self.scraping_chain = LLMChain(llm=llm, prompt=self.scraping_prompt)
        self.email_chain = LLMChain(llm=llm, prompt=self.email_prompt)

        self.scraping_tool = FacultyScrapingTool()
        self.email_tool = EmailCampaignTool()

    def execute_workflow(self):
        print("🚀 STARTING LANGCHAIN SEQUENTIAL WORKFLOW")
        print("=" * 60)

        try:
            scraping_result = self.scraping_tool._run("https://www.uow.edu.pk/Views/faculties/faculty?id=1")
            print(f"📊 Scraping Result: {scraping_result}")

            email_result = self.email_tool._run("faculty_profiles.csv", test_recipient)
            print(f"📧 Email Result: {email_result}")

            final_result = f"Workflow completed successfully!\n\nScraping: {scraping_result}\nEmails: {email_result}"

            print("\n" + "=" * 60)
            print("🎉 SEQUENTIAL WORKFLOW COMPLETED!")
            print("=" * 60)
            print("\n📋 FINAL RESULTS:")
            print(final_result)

            return final_result

        except Exception as e:
            print(f"\n❌ Sequential Workflow failed with error: {str(e)}")
            return None
