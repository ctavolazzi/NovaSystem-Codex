import os
import base64
import pickle
import json
import logging
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process
from crewai_tools import BaseTool
from langchain_community.llms import Ollama  # Ensure this import is correct based on your environment
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Gmail API configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

# Assuming instantiation of local_llm is successful
local_llm = Ollama(model=os.getenv('MODEL'))


class FetchLatestEmailTool(BaseTool):
    name: str = "Fetch Latest Email"
    description: str = "Fetches the latest unread email from the inbox."

    def _run(self, query: str = "is:unread") -> Dict[str, str]:
        """Return the latest unread email matching the optional Gmail search query."""
        service = get_gmail_service()
        try:
            email_details = fetch_latest_unread_email(service, query=query)
            if not email_details:
                return {"error": "No new unread emails found."}
            return email_details
        except HttpError as error:
            logging.error("Failed to fetch the latest email: %s", error)
            return {"error": f"Failed to fetch email: {error}"}

class LLMRecommendationTool(BaseTool):
    name: str = "LLM Recommendation"
    description: str = "Analyzes email content and generates recommendations."

    def _run(self, email_content: Optional[Dict[str, str]] = None) -> str:
        """Generate a recommendation for the provided email content."""
        if not email_content:
            return "No email content provided for analysis."

        email_text = email_content.get("text") or email_content.get("body") or ""
        processed_content = (
            "Please analyze this email content and suggest actions:\n\n"
            f"{email_text}"
        )

        recommendation = local_llm.invoke(processed_content)
        if isinstance(recommendation, str):
            return recommendation
        try:
            return json.dumps(recommendation)
        except TypeError:
            return str(recommendation)



# Fetch the latest unread email
def fetch_latest_unread_email(service, query: str = "is:unread"):
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No unread messages found.')
            return None

        message_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()

        payload = msg['payload']
        headers = payload.get('headers', [])
        body = _extract_plain_text_body(payload)

        email_details = {
            "id": message_id,
            "snippet": msg.get('snippet', ''),
            "body": body,
            "text": body,
        }

        for header in headers:
            if header['name'] == 'Subject':
                email_details['subject'] = header['value']
            elif header['name'] == 'From':
                email_details['from'] = header['value']

        clear_unread_label(service, message_id)

        return email_details

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def _extract_plain_text_body(payload: Dict[str, Any]) -> str:
    """Extract the plain text portion of a Gmail message payload."""
    body_data: Optional[str] = None

    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            if mime_type == 'text/plain':
                body_data = part.get('body', {}).get('data')
                if body_data:
                    break
    if not body_data:
        body_data = payload.get('body', {}).get('data', '')

    if not body_data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(body_data)
    return decoded_bytes.decode('utf-8', errors='replace')


def clear_unread_label(service, message_id: str) -> None:
    """Remove the UNREAD label from the specified Gmail message."""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']},
        ).execute()
    except HttpError as error:
        logging.error("Failed to clear UNREAD label: %s", error)

# Simulate processing and making a recommendation
def process_email_and_recommend(email_details):
    # Placeholder for processing logic; in practice, this could involve analyzing the email's content
    # Here we simply make a basic recommendation based on the presence of a keyword
    instructions = "Please analyze this email content and suggest actions in English:\n\n"

    prompt = f"{instructions}{email_details['body']}"

    recommendation = local_llm.invoke(prompt)

    print(f"Recommendation: {recommendation}")
    return recommendation

# Define your agents
fetch_latest_email_tool = FetchLatestEmailTool()
llm_recommendation_tool = LLMRecommendationTool()

email_agent = Agent(
    role="Email Agent",
    goal="Process emails and generate actionable insights.",
    backstory="A sophisticated AI agent capable of understanding and categorizing emails.",
    llm=local_llm,
    tools=[fetch_latest_email_tool, llm_recommendation_tool],
    verbose=True
)

# Define tasks and crew
fetch_email_task = Task(
    description="Fetch the latest unread email.",
    expected_output="Email content as a dictionary.",
    agent=email_agent,
    tools=[fetch_latest_email_tool]
)

analyze_email_task = Task(
    description="Analyze email content and generate a recommendation.",
    expected_output="A recommendation string.",
    agent=email_agent,
    tools=[llm_recommendation_tool],
    context=[fetch_email_task]
)

save_email_task = Task(
    description="Compile email content and recommendation into a JSON object and save.",
    expected_output="Confirmation of JSON saved.",
    agent=email_agent,
    # tools=[SaveEmailAsJSONTool()],
    context=[analyze_email_task]
)


email_crew = Crew(
    agents=[email_agent],
    tasks=[fetch_email_task, analyze_email_task],
    process=Process.sequential
)

# async def main():
#     await email_crew.kickoff()

# if __name__ == "__main__":
#     asyncio.run(main())

def main():
    service = get_gmail_service()
    email_details = fetch_latest_unread_email(service)
    if email_details:
        print(json.dumps(email_details, indent=2))
        process_email_and_recommend(email_details)

if __name__ == "__main__":
    main()