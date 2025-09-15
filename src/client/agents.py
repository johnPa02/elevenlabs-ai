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
                        "pronunciation_dictionary_id": "fmSQDgY3XmOSk59WtNwo",
                        "version_id": "d5hgc8VoDBupZxFlHkai"
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
                        "pronunciation_dictionary_id": "fmSQDgY3XmOSk59WtNwo",
                        "version_id": "d5hgc8VoDBupZxFlHkai"
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
    #             "phone": "0933725681",
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

    # print(get_agent("agent_4701k4kq3119enmbvvkwz5cey2rm"))
    # first_message = "Alo, em gọi để đặt bàn tại nhà hàng mình."
    # system_prompt = load_prompt_template("booking/system_prompt_action.md")
    # agent = create_agent(
    #     first_message=first_message,
    #     system_prompt=system_prompt,
    #     voice_id="BUPPIXeDaJWBz696iXRS",
    #     name="Booking Action Agent"
    # )

    # agents = list_agents()
    # print(agents)
    # Tools booking intake: ["tool_9501k4ht04tzfkdt8qsc8vkz30b3", "tool_4701k4kqda9yfedb6vx44jk9258x"]
    # Intake Agent: agent_3801k4fbtmkvf739gwvz8rgj1nb3
    # Action Agent: agent_4701k4kq3119enmbvvkwz5cey2rm
    system_prompt = load_prompt_template("consent_agent/system_prompt.md")
    agent = update_agent(
        agent_id="agent_5401k3n6bqjhe5f8rehcp559f5t7",
        first_message="Chào anh, em là Thúy Kiều, Kiều xin phép xác nhận một số thông tin nhé.",
        system_prompt=system_prompt,
        voice_id="EUVwmLU6voiyIbWsrs8V",
        tool_ids=["tool_0701k4a6h312fk380tdrq8t97r0f"]
    )
    # loan_system_prompt = load_prompt_template("system_prompt_v1.md")
    # update_loan_agent(agent_id="agent_5601k3g7eh6jeddbvr27f492cs72", loan_system_prompt=loan_system_prompt)
