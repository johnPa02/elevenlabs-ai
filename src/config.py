from dotenv import load_dotenv
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

load_dotenv()

# Core credentials
agent_id = os.getenv("AGENT_ID")
e_api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("VOICE_ID")

# Twilio credentials
twilio_sid = os.getenv("TWILIO_SID")
twilio_token = os.getenv("TWILIO_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
to_phone_number = os.getenv("TO_PHONE_NUMBER")

# Server tool behavior
max_retries = int(os.getenv("MAX_RETRIES", "2"))
session_ttl_seconds = int(os.getenv("SESSION_TTL_SECONDS", "600"))  # 10 minutes default
