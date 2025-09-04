import json
import os
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import signal
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from dotenv import load_dotenv
load_dotenv()

agent_id = "agent_5401k3n6bqjhe5f8rehcp559f5t7"
api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)
voice_id = "EUVwmLU6voiyIbWsrs8V"

customer_data = {
    "ten": "Nguyễn Thị Cam",
    "cccd": "528981176214",
    "dob": "18-09-1989",
    "phone": "0955423314"
}
MAX_RETRIES = 2
retry_count = 1

def confirm_identity(parameters):
    global retry_count
    name = (parameters.get("name") or "").strip()
    cccd = (parameters.get("cccd") or "").strip()
    phone = (parameters.get("phone") or "").strip()
    dob = (parameters.get("dob") or "").strip()
    print(f"Agent received parameters: name={name}, cccd={cccd}, phone={phone}, dob={dob}")

    if ((name == customer_data["ten"] and
            cccd == customer_data["cccd"] and
            phone == customer_data["phone"]) and
            dob == customer_data["dob"]):
        result = {"verified": True}
    else:
        retry_count += 1
        if retry_count > MAX_RETRIES:
            print("Maximum retries reached. Verification failed.")
            result = {"verified": False, "locked": True}
        else:
            result = {"verified": False, "locked": False}
    print(f"Tool returning: {result}")
    return json.dumps(result)

client_tools = ClientTools()
client_tools.register("confirmIdentity", confirm_identity)

conversation = Conversation(
    client=ElevenLabs(api_key=api_key),
    agent_id=agent_id,
    client_tools=client_tools,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
)

conversation.start_session()
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")

