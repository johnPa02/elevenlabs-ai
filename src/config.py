from dotenv import load_dotenv
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

load_dotenv()

# Core credentials
agent_id = os.getenv("AGENT_ID")
e_api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("VOICE_ID")

# Server tool behavior
max_retries = int(os.getenv("MAX_RETRIES", "2"))
session_ttl_seconds = int(os.getenv("SESSION_TTL_SECONDS", "600"))  # 10 minutes default
