import os
import time
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from config import sender_email, sender_password

class EmailCampaignInput(BaseModel):
    csv_file: str = Field(description="CSV file containing faculty data")
    test_email: str = Field(description="Test email address to send all emails to")

class EmailCampaignTool(BaseTool):
    name: str = "send_personalized_emails"
    description: str = "Generates and sends personalized emails to faculty members"
    args_schema: Type[BaseModel] = EmailCampaignInput

    def _run(self, csv_file: str, test_email: str) -> str:
        """Generate and send personalized emails based on faculty data."""
        print("📧 Starting email generation and sending...")

        try:
            if not os.path.exists(csv_file):
                error_msg = f"{csv_file} not found! Please scrape data first."
                print(f"❌ {error_msg}")
                return error_msg

            df = pd.read_csv(csv_file)
            print(f"📋 Loaded {len(df)} faculty profiles")

            successful_sends = 0
            failed_sends = 0

            # Email template
            email_template = """Dear Professor {name},

I hope this email finds you well. I am writing to express my interest in pursuing a Master's degree in Computer Science at the University of Wollongong.

I have reviewed your academic background ({qualification}) and was particularly drawn to your research in {research_interests}. Your work in this area aligns closely with my academic interests and career aspirations.

I would be grateful if you could provide information about:
- Available research opportunities in your lab
- MS program requirements and application process
- Potential funding opportunities for graduate students

I have strong academic credentials and would be happy to provide my transcripts and additional materials upon request.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Prospective Student]

---
TEST EMAIL NOTICE:
This is a test email sent to {test_email}
Original intended recipient: Professor {name}
Original email: {email}"""

            for idx, row in df.iterrows():
                try:
                    email_body = email_template.format(
                        name=row['Name'],
                        qualification=row['Qualification'],
                        research_interests=row['Research Interests'],
                        test_email=test_email,
                        email=row['Email']
                    )

                    print(f"\n📝 Generated email for {row['Name']}")

                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = test_email
                    msg["Subject"] = f"MS Application Inquiry - Test for Prof. {row['Name']}"
                    msg.attach(MIMEText(email_body, "plain"))

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, test_email, msg.as_string())

                    successful_sends += 1
                    print(f"✅ Email for {row['Name']} sent successfully!")
                    time.sleep(2)  # Rate limiting

                except Exception as e:
                    failed_sends += 1
                    print(f"❌ Failed to send email for {row['Name']}: {e}")

            summary = f"Email campaign completed! Successful: {successful_sends}, Failed: {failed_sends}"
            print(f"\n📊 EMAIL SUMMARY:")
            print(f"✅ Successful sends: {successful_sends}")
            print(f"❌ Failed sends: {failed_sends}")
            print(f"📧 All emails sent to: {test_email}")

            return summary

        except Exception as e:
            error_msg = f"Error in email process: {e}"
            print(f"❌ {error_msg}")
            return error_msg

    def _arun(self, csv_file: str, test_email: str) -> str:
        raise NotImplementedError("Async not implemented")
