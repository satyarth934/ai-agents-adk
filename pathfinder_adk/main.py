# main.py (Upgraded)
# The main script to run our ADK-powered feasibility agent.

import asyncio
from dotenv import load_dotenv

# Load environment variables from the .env file FIRST.
load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Setup Services and Runner
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="pathfinder_app",
    session_service=session_service
)

# Define the Asynchronous Interaction Logic
async def interact_with_agent(query: str):
    session = await session_service.create_session(
        app_name="pathfinder_app",
        user_id="test_user"
    )
    print(f"\n--- Running query in session: {session.id} ---")
    print(f">>> User: {query}")

    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response = "Agent did not provide a final answer."
    events = runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content
    )

    async for event in events:
        # --- NEW: Print the author of every event to see the full flow ---
        print(f"\n[Event] From: {event.author}")

        # For this complex agent, let's print more details to see its thought process.
        if event.get_function_calls():
            for call in event.get_function_calls():
                print(f"  ┗━ [Agent Action] Wants to call tool: '{call.name}'")
                print(f"     ┗━ With args: {call.args if len(str(call.args)) > 200 else '...'}")
        
        # --- NEW: Check for Tool Responses (The result of the action) ---
        if event.get_function_responses():
            for response in event.get_function_responses():
                print(f"  ┗━ [Tool Result] Tool '{response.name}' returned:")
                # Pretty print the dictionary response for readability
                import json
                print(f"     ┗━ {json.dumps(response.response, indent=2)}")
        
        # breakpoint()

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text.strip()
            break

    print(f"\n<<< Agent Final Report >>>\n{final_response}")

# Main Execution Block
async def main():
    print("--- Pathfinder ADK Agent (Feasibility Study) ---")
    # A more complex, natural language query for our upgraded agent
    # feasibility_query = "Please conduct a feasibility study for a new road connecting the Golden Gate Bridge in San Francisco to the city of Sausalito, CA."
    
    src_address = "5055 Santa Teresa Blvd, Gilroy, CA 95020"
    dst_address = "5530 Monterey Rd, Gilroy, CA 95020"
    feasibility_query = f"Please conduct a feasibility study for a new road connecting the {src_address} to {dst_address}."
    
    await interact_with_agent(feasibility_query)

if __name__ == "__main__":
    asyncio.run(main())