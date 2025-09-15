from src import config
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key=config.e_api_key,
)
print(client.voices.share(
    public_user_id="c81f7a40f0e2a40a5a99f6122b5d7a8a7f54aa45e6845f3d4dff9a79bf100fd8",
    voice_id="EUVwmLU6voiyIbWsrs8V",
    new_name="Vikkai Pro",
))
