import httpx
from src import config
from src.config import agent_id
from elevenlabs import ElevenLabs, OutboundSipTrunkConfigRequestModel
from elevenlabs.conversational_ai.phone_numbers import (
    PhoneNumbersCreateRequestBody_SipTrunk
)

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
    print(r.text)
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
    # from elevenlabs import ElevenLabs
    #
    client = ElevenLabs(
        api_key=config.e_api_key,
    )
    # client.conversational_ai.phone_numbers.create(
    #     request=PhoneNumbersCreateRequestBody_SipTrunk(
    #         phone_number="+12083303183",
    #         label="Alo",
    #         outbound_trunk_config=OutboundSipTrunkConfigRequestModel(
    #             address="sip:lumination@lumina-41a3eea89511.sip.signalwire.com"
    #         )
    #     ),
    # )
    # print(client.conversational_ai.phone_numbers.list())
    # client.conversational_ai.phone_numbers.update(
    #     phone_number_id="phnum_6201k4xzfg5qe8kacjr2s4475wv9",
    #     agent_id="agent_4701k4kq3119enmbvvkwz5cey2rm",
    # )
    # print(client.conversational_ai.sip_trunk.outbound_call(
    #     agent_id="agent_4701k4kq3119enmbvvkwz5cey2rm",
    #     agent_phone_number_id="phnum_6201k4xzfg5qe8kacjr2s4475wv9",
    #     to_number=config.to_phone_number,
    # ))
    # print(client.conversational_ai.phone_numbers.delete(
    #     phone_number_id="phnum_3201k4vcpw0xfcebk5vrgerzrncp",
    # ))
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
    #     phone_number="+14722125928",
    #     label="John",
    #     sid="ACc5ff0d6deb4d4542406db6b16cb99ba1",
    #     token="016adeda7c9891526cf406a7236636ea"))
    # print(update_phone_number("phnum_2301k4y1w7a2es3811c6wg1t0m0n", "agent_4701k4kq3119enmbvvkwz5cey2rm"))
    # WARNING: NEVER CALL IN LOCAL !!!
    # print(outbound_call(
    #     agent_id="agent_4701k4kq3119enmbvvkwz5cey2rm",
    #     agent_phone_number_id="phnum_3201k4vcpw0xfcebk5vrgerzrncp",
    #     to_number=to_number,
    #     dynamic_variables= {
    #         "booking_info": """{
    #             "date": "2025-09-12",
    #             "time": "19:00",
    #             "guests": 2,
    #             "name": "Vũ Hùng Cường",
    #             "phone": "0933725681",
    #             "notes": "Prefer window seat"
    #         }"""
    #     })
    # )
