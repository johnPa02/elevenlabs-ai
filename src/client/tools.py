import httpx
from src import config
BASE_URL = "https://api.elevenlabs.io/v1/convai"

headers = {
    "xi-api-key": config.e_api_key,
    "Content-Type": "application/json"
}

def create_tool(name, description, url):
    payload = {
        "tool_config":
            {
                "type": "webhook",
                "name": "confirmIdentity",
                "description": "Call this tool to verify customer identification information, including: name, cccd, phone, dob.",
                "response_timeout_secs": 20,
                "disable_interruptions": False,
                "force_pre_tool_speech": False,
                "assignments": [],
                "api_schema": {
                    "url": "https://api.voice.zeedata.io/tools/confirm-identity",
                    "method": "POST",
                    "path_params_schema": {},
                    "query_params_schema": None,
                    "request_body_schema": {
                        "type": "object",
                        "required": [
                            "name",
                            "cccd",
                            "dob",
                            "phone"
                        ],
                        "description": "The assistant should extract the customer's identity information from the transcript (full name, citizen ID number, date of birth, and phone number) and include them in this request body for verification.",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Full name as spoken by the customer in Vietnamese, including both family name and given name.",
                                "dynamic_variable": "",
                                "constant_value": ""
                            },
                            "cccd": {
                                "type": "string",
                                "description": "Extract the citizen identification number (CCCD) provided by the customer. Usually 12 digits",
                                "dynamic_variable": "",
                                "constant_value": ""
                            },
                            "dob": {
                                "type": "string",
                                "description": "Date of birth in DD-MM-YYYY format.",
                                "dynamic_variable": "",
                                "constant_value": ""
                            },
                            "phone": {
                                "type": "string",
                                "description": "Phone number provided by the customer.",
                                "dynamic_variable": "",
                                "constant_value": ""
                            }
                        }
                    },
                    "request_headers": {},
                    "auth_connection": None
                },
                "dynamic_variables": {
                    "dynamic_variable_placeholders": {}
                }
            }
        }

    r = httpx.post(f"{BASE_URL}/tools", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    name = "confirmIdentity"
    description = "Call this tool to verify customer identification information, including: name, cccd, phone, dob."
    url = "http://54.255.219.98:8101/tools/confirm-identity"
    tool = create_tool(name, description, url)
    print(tool)
