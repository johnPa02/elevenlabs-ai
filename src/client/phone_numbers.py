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
        token
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
        dynamic_variables=None,
) -> dict:
    """
    Make an outbound call using a specified agent and phone number.
    """
    if dynamic_variables:
        payload = {
            "agent_id": agent_id,
            "agent_phone_number_id": agent_phone_number_id,
            "to_number": to_number,
            "conversation_initiation_client_data": {
                "dynamic_variables": dynamic_variables
            }
        }
    else:
        payload = {
            "agent_id": agent_id,
            "agent_phone_number_id": agent_phone_number_id,
            "to_number": to_number
        }
    r = httpx.post(f"{BASE_URL}/twilio/outbound-call", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    # phone_number = "+16592349090"
    # label = "Thuy Kieu"
    # sid = config.twilio_sid
    # token = config.twilio_token
    # phone_number_id = config.phone_number_id
    to_number = config.to_phone_number
    # agent_id = config.agent_id
    # loan_agent_id = "agent_5601k3g7eh6jeddbvr27f492cs72"
    # dynamic_variables = {
    #     "ten": "Hoàng Anh",
    #     "so_hop_dong": "838191",
    #     "gioi_tinh": "Nữ",
    #     "khoan_vay": "20000000",
    #     "tien_thanh_toan": "2000000",
    #     "han_thanh_toan": "30-09-2025",
    #     "trang_thai": "Chưa thanh toán",
    #     "prefix": "chị"
    # }
    # print(create_twilio_phone_number(
    #     "+19786794308",
    #     "Kina",
    #     "AC512c0c29ae6ec8120004ee07178148f2",
    #     "cced382c30c81979e1ce0b82ac269657"))
    # print(update_phone_number("phnum_7701k4mdn82wff19adrhdxh2nkja", "agent_4701k4kq3119enmbvvkwz5cey2rm"))
    print(outbound_call(
        agent_id="agent_4701k4kq3119enmbvvkwz5cey2rm",
        agent_phone_number_id="phnum_7701k4mdn82wff19adrhdxh2nkja",
        to_number=to_number,
        dynamic_variables= {
            "booking_info": """{
                "date": "2025-09-12",
                "time": "19:00",
                "guests": 2,
                "name": "Vũ Hùng Cường",
                "phone": "0933725681",
                "notes": "Prefer window seat"
            }"""
        })
    )
