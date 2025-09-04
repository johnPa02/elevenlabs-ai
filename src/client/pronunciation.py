from warnings import catch_warnings

import httpx

from src import config


async def create_pronunciation_dictionary_from_rules():
    async with httpx.AsyncClient() as client:
        url = "https://api.elevenlabs.io/v1/pronunciation-dictionaries/add-from-rules"

        headers = {
            "xi-api-key": config.e_api_key,
            "Content-Type": "application/json"
        }

        data = {
            "name": "My Custom Dictionary",
            "rules": [
                {
                    "type": "alias",
                    "string_to_replace": "Cam",
                    "alias": "Ca-m"
                },
                {
                    "type": "alias",
                    "string_to_replace": "cam",
                    "alias": "ca-m"
                },
                {
                    "type": "alias",
                    "string_to_replace": "My",
                    "alias": "Myy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "my",
                    "alias": "myy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "mi",
                    "alias": "mii"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Mi",
                    "alias": "Mii"
                }
            ]
        }

        response = await client.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Created dictionary with ID: {result['id']}")
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_pronunciation_dictionary_from_rules())
