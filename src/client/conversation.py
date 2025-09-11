from elevenlabs import ElevenLabs

from src import config

client = ElevenLabs(
    api_key=config.e_api_key,
)
# print(client.conversational_ai.conversations.list().conversations[0])
def format_conversation(transcript):
    for i, turn in enumerate(transcript):
        print(f"--- Turn {i+1} ---")
        print(f"Role: {turn.role}")
        if turn.message:
            print(f"Message: {turn.message}")
        if turn.tool_calls:
            print("Tool Calls:")
            for call in turn.tool_calls:
                print(f"  - Tool Name: {call.tool_name}")
                print(f"    Params: {call.params_as_json}")
                if hasattr(call, 'tool_details') and call.tool_details:
                    print(f"    Details: {call.tool_details}")
        if turn.tool_results:
            print("Tool Results:")
            for result in turn.tool_results:
                print(f"  - Tool Name: {result.tool_name}")
                print(f"    Result: {result.result_value}")
                print(f"    Is Error: {result.is_error}")
        print()
# print(format_conversation(client.conversational_ai.conversations.get(
#     conversation_id="conv_8401k4fe2zq2ehn8xbn0ca5fb8db",
# ).transcript))

def get_lastest_conversation():
    conversations = client.conversational_ai.conversations.list().conversations[1]
    agent_name = conversations.agent_name
    conversation_id = conversations.conversation_id
    title = conversations.call_summary_title
    print(f"Agent Name: {agent_name}, Conversation ID: {conversation_id}, Title: {title}")
    print(format_conversation(client.conversational_ai.conversations.get(
        conversation_id=conversation_id,
    ).transcript))

if __name__ == "__main__":
    get_lastest_conversation()

