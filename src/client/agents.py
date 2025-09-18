import base64
import json
from urllib.parse import urlencode
from src import config
import httpx
import requests
from src.utils.prompt_utils import load_prompt_template


def generate_talk_to_url(agent_id, variables):
    """Generate URL with base64-encoded variables"""
    base_url = "https://elevenlabs.io/app/talk-to"
    encoded_vars = base64.b64encode(json.dumps(variables).encode()).decode()
    return f"{base_url}?agent_id={agent_id}&vars={encoded_vars}"

def generate_talk_to_url_with_params(agent_id, variables):
    """Generate URL with individual var_ parameters"""
    base_url = "https://elevenlabs.io/app/talk-to"
    params = {"agent_id": agent_id}

    for key, value in variables.items():
        params[f"var_{key}"] = value

    return f"{base_url}?{urlencode(params)}"

# ten = "Hoàng Anh"
# gioi_tinh = "Nữ"
# prefix = "chị"
#
# customer_info = {
#     "ten": ten,
#     "so_hop_dong": "A838191",
#     "gioi_tinh": gioi_tinh,
#     "khoan_vay": "20000000",
#     "tien_thanh_toan": "2000000",
#     "han_thanh_toan": "30-09-2025",
#     "trang_thai": "Chưa thanh toán",
#     "prefix": prefix
# }
#
# url_method1 = generate_talk_to_url("agent_6401k3bf3kfzfjzrfz1cgmmnnh87", customer_info)
# # url_method2 = generate_talk_to_url_with_params("your_agent_id", variables)
# print(url_method1)

BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": config.e_api_key,
    "Content-Type": "application/json"
}

def list_agents():
    r = httpx.get(f"{BASE_URL}/convai/agents", headers=headers)
    r.raise_for_status()
    return r.json()

def create_agent(first_message, system_prompt, voice_id, name):
    payload = {
        "conversation_config": {
            "tts": {
                "voice_id": voice_id,
                "model_id": "eleven_flash_v2_5",
                "optimize_streaming_latency": 3
            },
            "agent": {
                "first_message": first_message,
                "language": "vi",
                "prompt": {
                    "prompt": system_prompt
                },
            }
        },
        "name": name
    }
    r = requests.post(f"{BASE_URL}/convai/agents/create", headers=headers, json=payload)
    print("DEBUG response:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def update_agent(agent_id, first_message, system_prompt, voice_id, tool_ids=None):
    payload = {
        "conversation_config": {
            "asr": {
                "keywords": [
                    "The-gang", "Hokkaido", "The-gang-central", "Gangs", "Nguyễn", "Vũ",
                    "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Văn", "Đặng", "Bùi",
                    "Thị", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Trịnh", "Lương", "Đào"
                ]
            },
            "tts": {
                "voice_id": voice_id,
                "model_id": "eleven_flash_v2_5",
                "pronunciation_dictionary_locators": [
                    {
                        "pronunciation_dictionary_id": "H8Ku1teiGjBan1TTbSFH",
                        "version_id": "2XeWizi6t6BrsO9jRnQA"
                    }
                ],
                "optimize_streaming_latency": 3
            },
            "agent": {
                "first_message": first_message,
                "language": "vi",
                "prompt": {
                    "prompt": system_prompt,
                    "llm": "gpt-4o",
                    "tool_ids": tool_ids if tool_ids else []
                },
            }
        },
    }
    r = requests.patch(f"{BASE_URL}/convai/agents/{agent_id}", headers=headers, json=payload)
    print("DEBUG response:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def update_loan_agent(agent_id, loan_system_prompt, tool_ids=None):
    payload = {
        "conversation_config": {
            "asr": {
                "keywords": [
                    "The-gang", "Hokkaido", "The-gang-central", "Gangs", "Nguyễn", "Vũ",
                    "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Văn", "Đặng", "Bùi",
                    "Thị", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Trịnh", "Lương", "Đào"
                ]
            },
            "tts": {
                "voice_id": "BUPPIXeDaJWBz696iXRS",
                "model_id": "eleven_flash_v2_5",
                "pronunciation_dictionary_locators": [
                    {
                        "pronunciation_dictionary_id": "zV1iahRG2pfOPQy3sYns",
                        "version_id": "4RM0smcsIWvr35GF90DF"
                    }
                ],
            },
            "agent": {
                "language": "vi",
                "prompt": {
                    "prompt": loan_system_prompt,
                    "llm": "gpt-4o",
                    "tool_ids": tool_ids if tool_ids else []
                },
            }
        },
    }
    r = requests.patch(f"{BASE_URL}/convai/agents/{agent_id}", headers=headers, json=payload)
    print("DEBUG response:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def get_agent(agent_id):
    r = requests.get(f"{BASE_URL}/convai/agents/{agent_id}", headers=headers)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    # url_method1 = generate_talk_to_url(
    #     "agent_4701k4kq3119enmbvvkwz5cey2rm",
    #     {
    #         "booking_info": """{
    #             "date": "2025-09-12",
    #             "time": "19:00",
    #             "guests": 2,
    #             "name": "Vũ Hùng Cường",
    #             "phone": "0933-725-681",
    #             "notes": "Prefer window seat"
    #         }"""
    #     })
    # print(url_method1)
    # url_method1 = generate_talk_to_url(
    #     "agent_5601k3g7eh6jeddbvr27f492cs72",
    #     {
    #         "ten": "Hoàng Anh",
    #         "so_hop_dong": "A-8-3-8-1-9-1",
    #         "gioi_tinh": "Nữ",
    #         "khoan_vay": "20 triệu đồng",
    #         "tien_thanh_toan": "2 triệu đồng",
    #         "han_thanh_toan": "30-10-2025",
    #         "trang_thai": "Chưa thanh toán",
    #         "prefix": "chị"
    #     })
    # print(url_method1)
    # url_booking = generate_talk_to_url(
    #     "agent_3701k58xq6kzf7p973h18xbyy9ga",
    #     {
    #         "fullname": "Vũ Hùng Cường",
    #         "email": "quan@gmail.com",
    #         "phone": "0933-725-681",
    #         "date": "12-09-2025",
    #         "time": "19:00",
    #         "size": "2",
    #         "note": "Prefer window seat"
    #     })
    # print(url_booking)

    print(get_agent("agent_3801k4fbtmkvf739gwvz8rgj1nb3"))
    # first_message = "Alo, có phải chị vừa đặt bàn tại nhà hàng The Gangs không ạ?"
    # system_prompt = load_prompt_template("booking/system_prompt_consent.md")
    # agent = create_agent(
    #     first_message=first_message,
    #     system_prompt=system_prompt,
    #     voice_id="BUPPIXeDaJWBz696iXRS",
    #     name="Booking Consent Agent"
    # )

    # agents = list_agents()
    # print(agents)
    # Tools booking intake: ["tool_9501k4ht04tzfkdt8qsc8vkz30b3", "tool_4701k4kqda9yfedb6vx44jk9258x"]
    # Intake Agent: agent_3801k4fbtmkvf739gwvz8rgj1nb3
    # Action Agent: agent_4701k4kq3119enmbvvkwz5cey2rm
    # Consent: agent_3701k58xq6kzf7p973h18xbyy9ga
    # system_prompt = load_prompt_template("booking/system_prompt_consent.md")
    # agent = update_agent(
    #     agent_id="agent_3701k58xq6kzf7p973h18xbyy9ga",
    #     first_message="Chào anh, em gọi từ nhà hàng The Gangs. Anh vừa đặt bàn phải không ạ?",
    #     system_prompt=system_prompt,
    #     voice_id="EUVwmLU6voiyIbWsrs8V",
    #     tool_ids=[]
    # )
    # loan_system_prompt = load_prompt_template("system_prompt_v1.md")
    # update_loan_agent(agent_id="agent_5601k3g7eh6jeddbvr27f492cs72", loan_system_prompt=loan_system_prompt)
