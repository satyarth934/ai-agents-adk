# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='<FILL_IN_MODEL>',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )







# # agent.py
# # This file contains the Agent that orchestrates the workflow.

# import time
# from shapely.geometry import LineString
# import geopandas as gpd

# # Import all the tools the agent can use
# from tools import (
#     fetch_geospatial_data,
#     analyze_cost,
#     analyze_social_impact,
#     analyze_opportunity,
#     generate_report
# )

# class FeasibilityAgent:
#     def __init__(self):
#         self.memory = {} # Agent's memory to store results from tools

#     def run(self, point_a, point_b):
#         """Runs the entire feasibility study workflow."""
        
#         # --- THOUGHT & PLAN ---
#         print("[AGENT] Thought: I have received a new feasibility request. I need to formulate a plan.")
#         time.sleep(1)
#         print("""[AGENT] Plan:
# 1.  Fetch all relevant geospatial data for the area of interest.
# 2.  Analyze the construction cost and environmental difficulty.
# 3.  Analyze the social impact by checking for building displacement.
# 4.  Analyze the economic opportunity created by the new link.
# 5.  Synthesize all findings into a final visual report.
# I will now begin executing the plan.""")
#         print("-" * 30)
#         time.sleep(2)

#         # Store initial inputs
#         road_line_wgs84 = LineString([point_a[::-1], point_b[::-1]]) # Geo libraries often use (lon, lat)
#         self.memory['inputs'] = {'point_a': point_a, 'point_b': point_b, 'road_line_wgs84': road_line_wgs84}

#         # --- EXECUTION LOOP (Action -> Observation) ---

#         # Step 1: Fetch Data
#         print("[AGENT] Action: Calling GeospatialDataFetcher tool.")
#         time.sleep(1)
#         geospatial_data = fetch_geospatial_data(point_a, point_b)
#         if not geospatial_data:
#             print("[AGENT] Observation: Failed to fetch data. Aborting mission.")
#             return
#         self.memory['data'] = geospatial_data
#         print(f"[AGENT] Observation: Successfully fetched data. Found {len(geospatial_data['buildings'])} buildings and {len(geospatial_data['amenities'])} amenities.")
#         print("-" * 30)
#         time.sleep(1)
        
#         # For accurate distance/area calculations, we need to project our data
#         # WGS84 (lat/lon) uses degrees, which is bad for distance. UTM uses meters.
#         gdf_wgs84 = gpd.GeoDataFrame([{'geometry': road_line_wgs84}], crs="EPSG:4326")
#         gdf_utm = gdf_wgs84.to_crs("EPSG:3857") # Project to UTM (meters)
#         road_line_m = gdf_utm.iloc[0].geometry
        
#         # Project our fetched data too
#         for key in ['water', 'parks', 'amenities']:
#             self.memory['data'][key] = self.memory['data'][key].to_crs("EPSG:3857")

#         # Step 2: Analyze Cost
#         print("[AGENT] Action: Calling CostAnalysisTool.")
#         time.sleep(1)
#         cost_result = analyze_cost(road_line_m, self.memory['data']['water'], self.memory['data']['parks'])
#         self.memory['cost'] = cost_result
#         print(f"[AGENT] Observation: Cost analysis complete. {cost_result['details']}")
#         print("-" * 30)
#         time.sleep(1)

#         # Step 3: Analyze Social Impact
#         print("[AGENT] Action: Calling SocialImpactTool.")
#         time.sleep(1)
#         social_result = analyze_social_impact(road_line_wgs84, self.memory['data']['buildings'])
#         self.memory['social_impact'] = social_result
#         print(f"[AGENT] Observation: Social impact analysis complete. Found {social_result['num_buildings_intersected']} affected buildings.")
#         print("-" * 30)
#         time.sleep(1)

#         # Step 4: Analyze Opportunity
#         print("[AGENT] Action: Calling OpportunityAnalysisTool.")
#         time.sleep(1)
#         opportunity_result = analyze_opportunity(road_line_m, self.memory['data']['amenities'])
#         self.memory['opportunity'] = opportunity_result
#         print(f"[AGENT] Observation: Opportunity analysis complete. Found {opportunity_result['amenities_in_reach']} new amenities in reach.")
#         print("-" * 30)
#         time.sleep(1)

#         # Step 5: Generate Report
#         print("[AGENT] Thought: I have gathered all the necessary analysis. I will now synthesize these findings.")
#         time.sleep(1)
#         print("[AGENT] Action: Calling ReportGeneratorTool.")
#         report_path = generate_report(self.memory)
#         print(f"[AGENT] Observation: Report generated successfully.")
#         print("-" * 30)
        
#         # --- FINAL ANSWER ---
#         print("\n[AGENT] Final Answer: The feasibility study is complete.")
#         print(f"The analysis found an estimated cost of ${self.memory['cost']['total_cost']:,.0f}, affecting {self.memory['social_impact']['num_buildings_intersected']} buildings.")
#         print(f"A detailed visual report is available at: {report_path}")
















# agent.py
# This file contains the Agent that orchestrates the workflow.
# VERSION 2: Corrects the print statement after the cost analysis step.

import time
from shapely.geometry import LineString
import geopandas as gpd

# Import all the tools the agent can use
from tools import (
    fetch_geospatial_data,
    analyze_cost,
    analyze_social_impact,
    analyze_opportunity,
    generate_report
)

class FeasibilityAgent:
    def __init__(self):
        self.memory = {} # Agent's memory to store results from tools

    def run(self, point_a, point_b):
        """Runs the entire feasibility study workflow."""
        
        print("[AGENT] Thought: I have received a new feasibility request. I need to formulate a plan.")
        time.sleep(1)
        print("""[AGENT] Plan:
1.  Fetch all relevant geospatial data for the area of interest.
2.  Analyze the construction cost and environmental difficulty.
3.  Analyze the social impact by checking for building displacement.
4.  Analyze the economic opportunity created by the new link.
5.  Synthesize all findings into a final visual report.
I will now begin executing the plan.""")
        print("-" * 30)
        time.sleep(2)

        road_line_wgs84 = LineString([point_a[::-1], point_b[::-1]])
        self.memory['inputs'] = {'point_a': point_a, 'point_b': point_b, 'road_line_wgs84': road_line_wgs84}

        # Step 1: Fetch Data
        print("[AGENT] Action: Calling GeospatialDataFetcher tool.")
        time.sleep(1)
        geospatial_data = fetch_geospatial_data(point_a, point_b)
        if not geospatial_data:
            print("[AGENT] Observation: Failed to fetch data. Aborting mission.")
            return
        self.memory['data'] = geospatial_data
        print(f"[AGENT] Observation: Successfully fetched data. Found {len(geospatial_data['buildings'])} buildings and {len(geospatial_data['amenities'])} amenities.")
        print("-" * 30)
        time.sleep(1)
        
        gdf_wgs84 = gpd.GeoDataFrame([{'geometry': road_line_wgs84}], crs="EPSG:4326")
        gdf_utm = gdf_wgs84.to_crs("EPSG:3857")
        road_line_m = gdf_utm.iloc[0].geometry
        
        # Step 2: Analyze Cost
        print("[AGENT] Action: Calling CostAnalysisTool.")
        time.sleep(1)
        cost_result = analyze_cost(road_line_m, self.memory['data']['water'], self.memory['data']['parks'])
        self.memory['cost'] = cost_result
        
        # The print statement now uses the new keys available in cost_result.
        print(f"[AGENT] Observation: Cost analysis complete. Est. Total Cost: ${cost_result['total_cost']:,.0f}")
        print("-" * 30)
        time.sleep(1)

        # Step 3: Analyze Social Impact
        print("[AGENT] Action: Calling SocialImpactTool.")
        time.sleep(1)
        social_result = analyze_social_impact(road_line_wgs84, self.memory['data']['buildings'])
        self.memory['social_impact'] = social_result
        print(f"[AGENT] Observation: Social impact analysis complete. Found {social_result['num_buildings_intersected']} affected buildings.")
        print("-" * 30)
        time.sleep(1)

        # Step 4: Analyze Opportunity
        print("[AGENT] Action: Calling OpportunityAnalysisTool.")
        time.sleep(1)
        opportunity_result = analyze_opportunity(self.memory['data']['amenities'])
        self.memory['opportunity'] = opportunity_result
        print(f"[AGENT] Observation: Opportunity analysis complete. Found {opportunity_result['amenities_in_reach']} new amenities in reach.")
        print("-" * 30)
        time.sleep(1)

        # Step 5: Generate Report
        print("[AGENT] Thought: I have gathered all the necessary analysis. I will now synthesize these findings.")
        time.sleep(1)
        print("[AGENT] Action: Calling ReportGeneratorTool.")
        report_path = generate_report(self.memory)
        print(f"[AGENT] Observation: Report generated successfully.")
        print("-" * 30)
        
        print("\n[AGENT] Final Answer: The feasibility study is complete.")
        print(f"The analysis found an estimated cost of ${self.memory['cost']['total_cost']:,.0f}, affecting {self.memory['social_impact']['num_buildings_intersected']} buildings.")
        print(f"A detailed visual report is available at: {report_path}")