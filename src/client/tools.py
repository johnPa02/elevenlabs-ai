import httpx
from src import config
BASE_URL = "https://api.elevenlabs.io/v1/convai"

headers = {
    "xi-api-key": config.e_api_key,
    "Content-Type": "application/json"
}

def create_tool(name, description, url):
    payload = {
        "tool_config": {
          "type": "webhook",
          "name": name,
          "description": description,
          "api_schema": {
            "url": url,
            "method": "POST",
            "path_params_schema": [],
            "query_params_schema": [],
            "request_body_schema": {
              "id": "body",
              "type": "object",
              "description": "The assistant should extract the customer's identity information from the transcript (full name, citizen ID number, date of birth, and phone number) and include them in this request body for verification.",
              "required": True,
              "properties": [
                {
                  "id": "cccd",
                  "type": "string",
                  "value_type": "llm_prompt",
                  "description": "Extract the citizen identification number (CCCD) provided by the customer. Usually 12 digits",
                  "dynamic_variable": "",
                  "constant_value": "",
                  "required": True
                },
                {
                  "id": "name",
                  "type": "string",
                  "value_type": "llm_prompt",
                  "description": "Full name as spoken by the customer in Vietnamese, including both family name and given name.",
                  "dynamic_variable": "",
                  "constant_value": "",
                  "required": True
                },
                {
                  "id": "dob",
                  "type": "string",
                  "value_type": "llm_prompt",
                  "description": "Date of birth in DD-MM-YYYY format.",
                  "dynamic_variable": "",
                  "constant_value": "",
                  "required": True
                },
                {
                  "id": "phone",
                  "type": "string",
                  "value_type": "llm_prompt",
                  "description": "Phone number provided by the customer.",
                  "dynamic_variable": "",
                  "constant_value": "",
                  "required": True
                }
              ],
              "dynamic_variable": "",
              "constant_value": "",
              "value_type": "llm_prompt"
            },
            "request_headers": [],
            "auth_connection": None
          },
          "dynamic_variables": {
            "dynamic_variable_placeholders": {}
          },
          "assignments": [],
          "disable_interruptions": False,
          "response_timeout_secs": 20,
          "force_pre_tool_speech": "auto"
        }
    }
    r = httpx.post(f"{BASE_URL}/tools", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    name = "confirmIdentity"
    description = "Call this tool to verify customer identification information, including: name, cccd, phone, dob."
    url = "https://your-server.com/verify"
    tool = create_tool(name, description, url)
    print(tool)
