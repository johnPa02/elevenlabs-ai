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

def create_agent(first_message, system_prompt, dynamic_variables, voice_id):
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
                    "prompt": system_prompt,
                    "llm": "gemini-2.5-flash-lite-preview-06-17",
                    "tool_ids": ["tool_1601k3n5qap5es989vf4xzdewb51"]
                },
                "dynamic_variables": {
                    "dynamic_variable_placeholders": dynamic_variables
                }
            }
        },
        "name": "Consent Agent",
    }
    r = requests.post(f"{BASE_URL}/convai/agents/create", headers=headers, json=payload)
    print("DEBUG response:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()

def update_agent(agent_id, first_message, system_prompt, voice_id):
    payload = {
        "conversation_config": {
            "tts": {
                "voice_id": voice_id,
                "model_id": "eleven_flash_v2_5",
                "pronunciation_dictionary_locators": [
                    {
                        "pronunciation_dictionary_id": "8kG5F0zu76Gr2k8oyS2x",
                        "version_id": "5kIfUFqx9ImLvAcgSccw"
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
                    "tool_ids": ["tool_5901k3qsqh9dfefr1fkk5r5y0rt6"]
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
    # url_method1 = generate_talk_to_url("agent_5601k3g7eh6jeddbvr27f492cs72", config.dynamic_variables)
    # print(url_method1)

    # print(get_agent(config.agent_id))
    # system_prompt = load_prompt_template("consent_agent/system_prompt.md")
    # agent = create_agent(
    #     first_message="Chào anh! Em là Thúy Kiều, Kiều xin phép xác nhận một số thông tin nhé!",
    #     dynamic_variables=None,
    #     system_prompt=system_prompt,
    #     voice_id=None,
    # )
    # print(agent)

    # agents = list_agents()
    # print(agents)
    system_prompt = load_prompt_template("consent_agent/system_prompt.md")
    agent = update_agent(
        agent_id=config.agent_id,
        first_message="Chào anh! Em là Thúy Kiều, Kiều xin phép xác nhận một số thông tin nhé!",
        system_prompt=system_prompt,
        voice_id="BUPPIXeDaJWBz696iXRS",
    )
    print(agent)

    # if not agents.get("agents"):
    #     print("⚠️ No agents found, creating one...")
    #     agent = create_agent(
    #         first_message=config.first_message,
    #         dynamic_variables=config.dynamic_variables,
    #         system_prompt=config.system_prompt,
    #         voice_id=config.voice_id
    #     )
    #     print(agent)
    # else:
    #     print("✅ Agents found:", agents)
