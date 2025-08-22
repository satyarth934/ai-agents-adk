# main.py
# This is the main script to run the agent.

from agent import FeasibilityAgent

if __name__ == "__main__":
    # --- DEFINE YOUR POINTS HERE ---
    # Using coordinates for Pittsburgh, USA - a city with interesting geography (rivers, parks, hills)
    # Coordinates are in (latitude, longitude) format
    
    # POINT_A = (40.457, -80.010) 
    # POINT_B = (40.453, -80.015)

    POINT_A = (37.8199109, -122.4785598)    # Golden gate bridge
    POINT_B = (37.8590937, -122.4852507)    # Sausalito

    print("--- Starting Pathfinder Agent ---")
    print(f"Analyzing proposed road from {POINT_A} to {POINT_B}\n")
    
    # Create an instance of the agent
    pathfinder = FeasibilityAgent()
    
    # Run the agent with the specified points
    pathfinder.run(point_a=POINT_A, point_b=POINT_B)
    
    print("\n--- Pathfinder Agent Finished ---")