# # agent.py
# # This file initializes the ADK agent with its tools and persona.

# from google.adk.agents import Agent
# from tools import get_coordinates_from_placename

# # 1. Define the root agent for our application
# # This is a direct instantiation of the Agent class.
# root_agent = Agent(
#     name="pathfinder_assistant",
#     model="gemini-2.5-flash", # Or your preferred Gemini model
#     description="An assistant that can find geographic coordinates.",
#     instruction="You are a helpful assistant. Answer user questions by finding the coordinates of places using your tools.",
#     tools=[get_coordinates_from_placename] # Pass the function directly
# )




# # agent.py (Upgraded)
# # This file initializes the ADK agent with its new, powerful persona.

# from google.adk.agents import Agent
# from tools import (
#     get_coordinates_from_placename,
#     fetch_geospatial_data,
#     analyze_feasibility_metrics
# )

# # Define the root agent for our application
# root_agent = Agent(
#     name="urban_planning_assistant",
#     model="gemini-2.5-flash", # A good model for multi-step reasoning
#     description="An expert AI assistant for conducting preliminary road feasibility studies.",
#     instruction="""You are an expert urban planning assistant. Your goal is to conduct a preliminary feasibility study for a new road link between two locations.

# Follow these steps precisely:
# 1.  When the user gives you two locations, use the 'get_coordinates_from_placename' tool for EACH location to find their exact latitude and longitude.
# 2.  Once you have the coordinates for both the start and end points, use the 'fetch_geospatial_data' tool to gather information about buildings, parks, and water along the proposed route.
# 3.  After you have the geospatial data, create a JSON string representing the straight-line road geometry between the start and end coordinates.
# 4.  Then, use the 'analyze_feasibility_metrics' tool, providing the road line JSON and the data you collected in the previous step.
# 5.  Finally, present the results from the analysis to the user in a clear, summarized format. Do not add any information not present in the tool's output.
# """,
#     tools=[
#         get_coordinates_from_placename,
#         fetch_geospatial_data,
#         analyze_feasibility_metrics
#     ]
# )






# # agent.py (Final Corrected Version)
# # This file initializes the ADK agent with a more capable model and clearer instructions.

# from google.adk.agents import Agent
# from tools import (
#     get_coordinates_from_placename,
#     fetch_geospatial_data,
#     analyze_feasibility_metrics
# )

# # Define the root agent for our application
# root_agent = Agent(
#     name="urban_planning_assistant",
    
#     # <<< CHANGE 1: Use a more powerful model for multi-step reasoning.
#     model="gemini-2.5-flash",
    
#     description="An expert AI assistant for conducting preliminary road feasibility studies.",
#     instruction="""You are an expert urban planning assistant. Your goal is to conduct a preliminary feasibility study for a new road link between two locations.

# Follow these steps precisely:
# 1.  When the user gives you two locations, use the 'get_coordinates_from_placename' tool for EACH location to find their exact latitude and longitude.
# 2.  Once you have the coordinates for both the start and end points, use the 'fetch_geospatial_data' tool to gather information about buildings, parks, and water along the proposed route.
# 3.  After you have the geospatial data, create a JSON string representing the straight-line road geometry between the start and end coordinates.
# 4.  Then, use the 'analyze_feasibility_metrics' tool, providing the road line JSON and the data you collected in the previous step.
# 5.  Finally, present the results from the analysis to the user in a clear, summarized format. Do not add any information not present in the tool's output.

# IMPORTANT: After the final analysis tool has run, your final answer MUST be a user-friendly summary of the results.
# """, # <<< CHANGE 2: Added a strong final instruction.
#     tools=[
#         get_coordinates_from_placename,
#         fetch_geospatial_data,
#         analyze_feasibility_metrics
#     ]
# )





# agent.py (Upgraded with State Management Workflow)

from google.adk.agents import Agent
from tools import (
    get_coordinates_from_placename,
    fetch_geospatial_data,
    # save_data_to_state, # <<< NEW
    analyze_feasibility_metrics_from_state # <<< UPDATED
)

# ------------------
# Instructions
# ------------------
# prompt_instructions = """You are an expert urban planning assistant. Your goal is to conduct a preliminary feasibility study for a new road link between two locations.

# Follow these steps precisely:
# 1.  When the user gives you two locations, use the 'get_coordinates_from_placename' tool for EACH location to find their exact latitude and longitude.
# 2.  Once you have the coordinates for both the start and end points, use the 'fetch_geospatial_data' tool to gather information about buildings, parks, and water along the proposed route, which will be ased into the session state.
# 3.  IMMEDIATELY after fetching the data, use the 'save_data_to_state' tool to save all the returned data (road_line_json, buildings_json, parks_json, water_json) into the session state. Do not modify the data.
# 4.  After the data has been successfully saved, use the 'analyze_feasibility_metrics_from_state' tool to perform the final analysis. This tool takes no arguments as it reads from the state.
# 5.  Finally, present the results from the analysis to the user in a clear, summarized format. Do not add any information not present in the tool's output.

# IMPORTANT: After the final analysis tool has run, your final answer MUST be a user-friendly summary of the results.
# """

prompt_instructions = """You are an expert urban planning assistant. Your goal is to conduct a preliminary feasibility study for a new road link between two locations.

Follow these steps precisely:
1.  When the user gives you two locations, use the 'get_coordinates_from_placename' tool for EACH location to find their exact latitude and longitude.
2.  Once you have the coordinates for both the start and end points, use the 'fetch_geospatial_data' tool to gather information about buildings, parks, and water along the proposed route, which will be ased into the session state.
3.  After the data has been successfully saved, use the 'analyze_feasibility_metrics_from_state' tool to perform the final analysis. This tool takes no arguments as it reads from the state.
4.  Finally, present the results from the analysis to the user in a clear, summarized format. Do not add any information not present in the tool's output.

IMPORTANT: After the final analysis tool has run, your final answer MUST be a user-friendly summary of the results.
"""


# Define the root agent for our application
root_agent = Agent(
    name="urban_planning_assistant",
    model="gemini-2.5-flash",
    description="An expert AI assistant for conducting preliminary road feasibility studies.",
    instruction=prompt_instructions,
    tools=[
        get_coordinates_from_placename,
        fetch_geospatial_data,
        # save_data_to_state, # <<< NEW
        analyze_feasibility_metrics_from_state # <<< UPDATED
    ]
)