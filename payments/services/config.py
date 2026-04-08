import os
from dotenv import load_dotenv

load_dotenv()

STRIPE_API_KEY=os.environ.get("STRIPE_API_KEY")
SLACK_WEBHOOK_URL=os.environ.get("SLACK_WEBHOOK_URL")