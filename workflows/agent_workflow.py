from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from tools.faculty_scraper import FacultyScrapingTool
from tools.email_campaign import EmailCampaignTool
from llm_setup import llm
from config import test_recipient

class EmailCampaignAgent:
    def __init__(self):
        self.scraping_tool = FacultyScrapingTool()
        self.email_tool = EmailCampaignTool()

        self.tools = [
            Tool(
                name="scrape_faculty_data",
                description="Scrapes faculty data from university website and saves to CSV. Input should be a URL.",
                func=lambda url: self.scraping_tool._run(url, "faculty_profiles.csv")
            ),
            Tool(
                name="send_personalized_emails",
                description="Sends personalized emails to faculty members from CSV data. Input should be 'csv_file,test_email'.",
                func=lambda input_str: self.email_tool._run(*input_str.split(',', 1))
            )
        ]

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.agent = initialize_agent(
            tools=self.tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

    def execute_campaign(self):
        print("🚀 STARTING LANGCHAIN EMAIL CAMPAIGN")
        print("=" * 60)
        print(f"📧 Target test inbox: {test_recipient}")
        print("=" * 60)

        try:
            workflow_prompt = f"""
            Execute a complete email campaign workflow:

            1. First, scrape faculty data from the University of Wollongong Computer Science department at: https://www.uow.edu.pk/Views/faculties/faculty?id=1
            2. Then, send personalized emails to all faculty members using the test email: {test_recipient}

            Make sure to complete both steps sequentially and provide a summary of the results.
            """

            result = self.agent.run(workflow_prompt)

            print("\n" + "=" * 60)
            print("🎉 LANGCHAIN CAMPAIGN COMPLETED!")
            print("=" * 60)
            print("\n📋 FINAL RESULTS:")
            print(result)

            return result

        except Exception as e:
            print(f"\n❌ LangChain Campaign failed with error: {str(e)}")
            return None
