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
            "name": "Custom Dictionary",
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
                },
                {
                    "type": "alias",
                    "string_to_replace": "Hạn",
                    "alias": "Hàn"
                },
                {
                    "type": "alias",
                    "string_to_replace": "hạn",
                    "alias": "hàn"
                },
                {
                    "type": "alias",
                    "string_to_replace": "4",
                    "alias": "bún"
                },
                {
                    "type": "alias",
                    "string_to_replace": "bốn",
                    "alias": "bún"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Bốn",
                    "alias": "bún"
                },
                {
                    "type": "alias",
                    "string_to_replace": "vay",
                    "alias": "vayy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Vay",
                    "alias": "vayy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "hiện",
                    "alias": "hìen"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Hiện",
                    "alias": "hìen"
                },
                {
                    "type": "alias",
                    "string_to_replace": "chị",
                    "alias": "trị"
                },
                {
                    "type": "alias",
                    "string_to_replace": "khoản",
                    "alias": "khoãn"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Khoản",
                    "alias": "khoãn"
                },
                {
                    "type": "alias",
                    "string_to_replace": "hai",
                    "alias": "hayy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Hai",
                    "alias": "Hayy"
                },
                {
                    "type": "alias",
                    "string_to_replace": "chủ",
                    "alias": "chù"
                },
                {
                    "type": "alias",
                    "string_to_replace": "Chủ",
                    "alias": "Chủ"
                },
                {
                    "type": "alias",
                    "string_to_replace": "bảy",
                    "alias": "bãi"
                },
                {
                    "type": "alias",
                    "string_to_replace": "tối",
                    "alias": "tói"
                },
                {
                    "type": "alias",
                    "string_to_replace": "đặt",
                    "alias": "book"
                },
                {
                    "type": "alias",
                    "string_to_replace": "chỗ",
                    "alias": "chồ"
                },
                {
                    "type": "alias",
                    "string_to_replace": "trống",
                    "alias": "chóng"
                }
            ]
        }

        response = await client.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Created dictionary with ID: {result}")
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_pronunciation_dictionary_from_rules())
