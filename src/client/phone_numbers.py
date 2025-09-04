import httpx
from src import config
from src.config import agent_id

BASE_URL = "https://api.elevenlabs.io/v1/convai"

headers = {
    "xi-api-key": config.e_api_key,
    "Content-Type": "application/json"
}

def create_twilio_phone_number(
        phone_number,
        label,
        sid,
        token,
) -> dict:
    """
    Create a Twilio phone number in ElevenLabs ConvAI.
    """
    payload = {
        "phone_number": phone_number,
        "label": label,
        "sid": sid,
        "token": token
    }
    r = httpx.post(f"{BASE_URL}/phone-numbers", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

def update_phone_number(
        phone_number_id,
        agent_id,
) -> dict:
    """
    Update the agent associated with a phone number.
    """
    payload = {
        "agent_id": agent_id
    }
    r = httpx.patch(f"{BASE_URL}/phone-numbers/{phone_number_id}", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

def outbound_call(
        agent_id,
        agent_phone_number_id,
        to_number,
) -> dict:
    """
    Make an outbound call using a specified agent and phone number.
    """
    payload = {
        "agent_id": agent_id,
        "agent_phone_number_id": agent_phone_number_id,
        "to_number": to_number
    }
    r = httpx.post(f"{BASE_URL}/twilio/outbound-call", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    phone_number = "+16592349090"
    label = "Thuy Kieu"
    sid = config.twilio_sid
    token = config.twilio_token
    phone_number_id = config.phone_number_id
    to_number = config.to_phone_number
    agent_id = config.agent_id

    # Uncomment to create/update/outbound based on your env
    # print(create_twilio_phone_number(phone_number, label, sid, token))
    # print(update_phone_number(phone_number_id, agent_id))
    print(outbound_call(agent_id=agent_id, agent_phone_number_id=phone_number_id, to_number=to_number))
