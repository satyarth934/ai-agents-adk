# # tools.py (Upgraded)
# # This file contains all specialized tools for our agent.

# import os
# import googlemaps
# from typing import List, Dict, Any

# from shapely.geometry import LineString
# import osmnx as ox
# import geopandas as gpd

# # Initialize the Google Maps client from the environment variable
# gmaps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))

# # --- Foundational Tool (from previous step) ---
# def get_coordinates_from_placename(place_name: str) -> str:
#     """
#     Finds the geographic coordinates (latitude, longitude) for a given place name.
#     Use this tool FIRST to get the precise coordinates for start and end points.

#     Args:
#         place_name (str): The name of the place to geocode.

#     Returns:
#         str: A formatted string with the coordinates or an error message.
#     """
#     try:
#         geocode_result = gmaps.geocode(place_name)
#         if not geocode_result:
#             return f"Could not find coordinates for {place_name}."
        
#         lat = geocode_result[0]['geometry']['location']['lat']
#         lng = geocode_result[0]['geometry']['location']['lng']
#         # Return a structured, machine-readable string
#         return f"Coordinates: (lat={lat}, lon={lng})"
#     except Exception as e:
#         return f"An error occurred while geocoding: {e}"


# # --- New Feasibility Analysis Tools ---

# def fetch_geospatial_data(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
#     """
#     Fetches geospatial data (buildings, parks, water) along a straight line corridor.
#     Use this tool AFTER getting coordinates to gather data for analysis.

#     Args:
#         start_lat (float): Latitude of the starting point.
#         start_lon (float): Longitude of the starting point.
#         end_lat (float): Latitude of the ending point.
#         end_lon (float): Longitude of the ending point.

#     Returns:
#         Dict[str, Any]: A dictionary containing GeoDataFrames for buildings, parks, and water.
#                          Returns an error message if data fetching fails.
#     """
#     try:
#         line_wgs84 = LineString([(start_lon, start_lat), (end_lon, end_lat)])
#         gdf_wgs84 = gpd.GeoDataFrame([{'geometry': line_wgs84}], crs="EPSG:4326")
#         gdf_utm = gdf_wgs84.to_crs("EPSG:3857")
#         buffer_utm = gdf_utm.buffer(200).iloc[0] # 200-meter buffer on each side

#         buffer_utm_gs = gpd.GeoSeries([buffer_utm], crs="EPSG:3857")
#         buffer_wgs84_gs = buffer_utm_gs.to_crs("EPSG:4326")
#         buffer_wgs84_polygon = buffer_wgs84_gs.iloc[0]

#         tags = {
#             "building": True, 
#             "natural": "water", 
#             "leisure": "park",
#         }
#         gdf = ox.features.features_from_polygon(buffer_wgs84_polygon, tags)
        
#         # We are returning the raw GeoDataFrame data as JSON. 
#         # A production system might process this further.
#         return {
#             "buildings_json": gdf[gdf['building'].notna()].to_json(),
#             "parks_json": gdf[gdf['leisure'] == 'park'].to_json(),
#             "water_json": gdf[gdf['natural'] == 'water'].to_json(),
#         }
#     except Exception as e:
#         return {"error": f"Failed to fetch geospatial data from OpenStreetMap: {e}"}


# def analyze_feasibility_metrics(road_line_json: str, buildings_json: str, parks_json: str, water_json: str) -> Dict[str, Any]:
#     """
#     Analyzes cost, social impact, and opportunity for a proposed road.
#     Use this tool as the main analysis step AFTER fetching geospatial data.

#     Args:
#         road_line_json (str): A JSON representation of the road's LineString geometry.
#         buildings_json (str): JSON representation of the building GeoDataFrame.
#         parks_json (str): JSON representation of the park GeoDataFrame.
#         water_json (str): JSON representation of the water GeoDataFrame.

#     Returns:
#         Dict[str, Any]: A dictionary containing a full quantitative analysis.
#     """

#     breakpoint()
#     try:
#         # Load geometries from JSON
#         road_line_gdf = gpd.read_file(road_line_json, driver='GeoJSON')
#         buildings_gdf = gpd.read_file(buildings_json, driver='GeoJSON')
#         parks_gdf = gpd.read_file(parks_json, driver='GeoJSON')
#         water_gdf = gpd.read_file(water_json, driver='GeoJSON')
        
#         # Ensure CRS is consistent for metric calculations (meters)
#         road_line_m = road_line_gdf.to_crs("EPSG:3857").iloc[0].geometry
#         water_m = water_gdf.to_crs("EPSG:3857")
#         parks_m = parks_gdf.to_crs("EPSG:3857")

#         # --- Cost Analysis ---
#         length_km = road_line_m.length / 1000
#         base_cost = length_km * 5_000_000 # $5M per km
#         water_crossings = water_m.intersection(road_line_m)
#         bridge_length_m = sum(g.length for g in water_crossings if not g.is_empty)
#         bridge_cost = bridge_length_m * 25_000 # $25k per meter for bridge
#         total_cost = base_cost + bridge_cost

#         # --- Social Impact Analysis ---
#         intersected_buildings = buildings_gdf[buildings_gdf.intersects(road_line_gdf.iloc[0].geometry)]
#         num_buildings_impacted = len(intersected_buildings)
        
#         # --- Environmental Impact ---
#         park_crossings = parks_m.intersection(road_line_m)
#         park_area_impacted_sqm = sum(g.area for g in park_crossings if not g.is_empty)

#         return {
#             "status": "Success",
#             "estimated_cost": f"${total_cost:,.0f}",
#             "road_length_km": f"{length_km:.2f}",
#             "social_impact": f"{num_buildings_impacted} buildings directly impacted.",
#             "environmental_impact": f"{park_area_impacted_sqm:,.0f} sq. meters of parkland impacted."
#         }
#     except Exception as e:
#         return {"error": f"An error occurred during analysis: {e}"}












# # tools.py (Corrected and More Robust)
# # This file contains all the specialized tools for our agent.

# import os
# import googlemaps
# from typing import List, Dict, Any

# from shapely.geometry import LineString
# import osmnx as ox
# import geopandas as gpd

# # Initialize the Google Maps client from the environment variable
# gmaps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))

# # --- Foundational Tool ---
# def get_coordinates_from_placename(place_name: str) -> str:
#     """
#     Finds the geographic coordinates (latitude, longitude) for a given place name.
#     Use this tool FIRST to get the precise coordinates for start and end points.

#     Args:
#         place_name (str): The name of the place to geocode.

#     Returns:
#         str: A formatted string with the coordinates or an error message.
#     """
#     try:
#         geocode_result = gmaps.geocode(place_name)
#         if not geocode_result:
#             return f"Could not find coordinates for {place_name}."
        
#         lat = geocode_result[0]['geometry']['location']['lat']
#         lng = geocode_result[0]['geometry']['location']['lng']
#         return f"Coordinates: (lat={lat}, lon={lng})"
#     except Exception as e:
#         return f"An error occurred while geocoding: {e}"


# # --- New Feasibility Analysis Tools ---

# def fetch_geospatial_data(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
#     """
#     Fetches geospatial data (buildings, parks, water) along a straight line corridor.
#     Use this tool AFTER getting coordinates to gather data for analysis.

#     Args:
#         start_lat (float): Latitude of the starting point.
#         start_lon (float): Longitude of the starting point.
#         end_lat (float): Latitude of the ending point.
#         end_lon (float): Longitude of the ending point.

#     Returns:
#         Dict[str, Any]: A dictionary containing GeoDataFrames for buildings, parks, and water.
#                          Returns an error message if data fetching fails.
#     """
#     try:
#         line_wgs84 = LineString([(start_lon, start_lat), (end_lon, end_lat)])
#         gdf_wgs84 = gpd.GeoDataFrame([{'geometry': line_wgs84}], crs="EPSG:4326")
#         gdf_utm = gdf_wgs84.to_crs("EPSG:3857")
#         buffer_utm = gdf_utm.buffer(200).iloc[0] # 200-meter buffer on each side

#         buffer_utm_gs = gpd.GeoSeries([buffer_utm], crs="EPSG:3857")
#         buffer_wgs84_gs = buffer_utm_gs.to_crs("EPSG:4326")
#         buffer_wgs84_polygon = buffer_wgs84_gs.iloc[0]

#         tags = {"building": True, "natural": "water", "leisure": "park"}
#         gdf = ox.features.features_from_polygon(buffer_wgs84_polygon, tags)
        
#         # --- THE FIX IS HERE ---
#         # We now check if each column exists before trying to filter on it.
#         # If a column doesn't exist, we create an empty GeoDataFrame.

#         if 'building' in gdf.columns:
#             buildings_gdf = gdf[gdf['building'].notna()]
#         else:
#             buildings_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         if 'leisure' in gdf.columns:
#             parks_gdf = gdf[gdf['leisure'] == 'park']
#         else:
#             parks_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         if 'natural' in gdf.columns:
#             water_gdf = gdf[gdf['natural'] == 'water']
#         else:
#             water_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         return {
#             "buildings_json": buildings_gdf.to_json(),
#             "parks_json": parks_gdf.to_json(),
#             "water_json": water_gdf.to_json(),
#         }
#     except Exception as e:
#         # Catching a broader exception range for robustness
#         return {"error": f"An unexpected error occurred in fetch_geospatial_data: {e}"}


# def analyze_feasibility_metrics(road_line_json: str, buildings_json: str, parks_json: str, water_json: str) -> Dict[str, Any]:
#     """
#     Analyzes cost, social impact, and opportunity for a proposed road.
#     Use this tool as the main analysis step AFTER fetching geospatial data.

#     Args:
#         road_line_json (str): A JSON representation of the road's LineString geometry.
#         buildings_json (str): JSON representation of the building GeoDataFrame.
#         parks_json (str): JSON representation of the park GeoDataFrame.
#         water_json (str): JSON representation of the water GeoDataFrame.

#     Returns:
#         Dict[str, Any]: A dictionary containing a full quantitative analysis.
#     """
#     try:
#         # Load geometries from JSON. gpd.read_file handles empty JSON gracefully.
#         road_line_gdf = gpd.read_file(road_line_json, driver='GeoJSON')
#         buildings_gdf = gpd.read_file(buildings_json, driver='GeoJSON')
#         parks_gdf = gpd.read_file(parks_json, driver='GeoJSON')
#         water_gdf = gpd.read_file(water_json, driver='GeoJSON')
        
#         # Ensure CRS is consistent for metric calculations (meters)
#         road_line_m = road_line_gdf.to_crs("EPSG:3857").iloc[0].geometry
#         water_m = water_gdf.to_crs("EPSG:3857")
#         parks_m = parks_gdf.to_crs("EPSG:3857")

#         # --- Cost Analysis ---
#         length_km = road_line_m.length / 1000
#         base_cost = length_km * 5_000_000 # $5M per km
#         bridge_length_m = 0
#         if not water_m.empty:
#             water_crossings = water_m.intersection(road_line_m)
#             bridge_length_m = sum(g.length for g in water_crossings if not g.is_empty)
#         bridge_cost = bridge_length_m * 25_000 # $25k per meter for bridge
#         total_cost = base_cost + bridge_cost

#         # --- Social Impact Analysis ---
#         num_buildings_impacted = 0
#         if not buildings_gdf.empty:
#             intersected_buildings = buildings_gdf[buildings_gdf.intersects(road_line_gdf.iloc[0].geometry)]
#             num_buildings_impacted = len(intersected_buildings)
        
#         # --- Environmental Impact ---
#         park_area_impacted_sqm = 0
#         if not parks_m.empty:
#             park_crossings = parks_m.intersection(road_line_m)
#             # Use area of the intersection polygon
#             park_area_impacted_sqm = sum(g.area for g in park_crossings if not g.is_empty)

#         return {
#             "status": "Success",
#             "estimated_cost": f"${total_cost:,.0f}",
#             "road_length_km": f"{length_km:.2f}",
#             "social_impact": f"{num_buildings_impacted} buildings directly impacted.",
#             "environmental_impact": f"{park_area_impacted_sqm:,.0f} sq. meters of parkland impacted."
#         }
#     except Exception as e:
#         return {"error": f"An error occurred during analysis: {e}"}









# # tools.py (Upgraded with Caching)
# # This file contains all specialized tools for our agent.

# import os
# import googlemaps
# import hashlib
# import json
# from typing import Dict, Any

# from shapely.geometry import LineString
# import osmnx as ox
# import geopandas as gpd

# # Initialize the Google Maps client from the environment variable
# gmaps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))

# # --- Foundational Tool ---
# def get_coordinates_from_placename(place_name: str) -> str:
#     """
#     Finds the geographic coordinates (latitude, longitude) for a given place name.
#     Use this tool FIRST to get the precise coordinates for start and end points.

#     Args:
#         place_name (str): The name of the place to geocode.

#     Returns:
#         str: A formatted string with the coordinates or an error message.
#     """
#     try:
#         geocode_result = gmaps.geocode(place_name)
#         if not geocode_result:
#             return f"Could not find coordinates for {place_name}."
        
#         lat = geocode_result[0]['geometry']['location']['lat']
#         lng = geocode_result[0]['geometry']['location']['lng']
#         return f"Coordinates: (lat={lat}, lon={lng})"
#     except Exception as e:
#         return f"An error occurred while geocoding: {e}"


# # --- New Feasibility Analysis Tools ---

# def fetch_geospatial_data(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
#     """
#     Fetches geospatial data (buildings, parks, water) along a straight line corridor.
#     This tool caches results locally to speed up repeated queries for the same route.
#     """
#     # --- CACHING LOGIC START ---
#     # Create a unique filename based on the coordinates
#     coords_str = f"{start_lat}{start_lon}{end_lat}{end_lon}"
#     hashed_filename = hashlib.md5(coords_str.encode()).hexdigest() + ".json"
#     cache_path = os.path.join("cache", hashed_filename)

#     # Check if the cache file exists
#     if os.path.exists(cache_path):
#         print(f"  [Tool Action] Loading geospatial data from cache: {cache_path}")
#         with open(cache_path, 'r') as f:
#             return json.load(f)
#     # --- CACHING LOGIC END ---

#     print("  [Tool Action] No cache found. Fetching data from OpenStreetMap API (this may take a few minutes)...")
#     try:
#         line_wgs84 = LineString([(start_lon, start_lat), (end_lon, end_lat)])
#         gdf_wgs84 = gpd.GeoDataFrame([{'geometry': line_wgs84}], crs="EPSG:4326")
#         gdf_utm = gdf_wgs84.to_crs("EPSG:3857")
#         buffer_utm = gdf_utm.buffer(200).iloc[0] # 200-meter buffer on each side

#         buffer_utm_gs = gpd.GeoSeries([buffer_utm], crs="EPSG:3857")
#         buffer_wgs84_gs = buffer_utm_gs.to_crs("EPSG:4326")
#         buffer_wgs84_polygon = buffer_wgs84_gs.iloc[0]

#         tags = {"building": True, "natural": "water", "leisure": "park"}
#         gdf = ox.features.features_from_polygon(buffer_wgs84_polygon, tags)
        
#         if 'building' in gdf.columns:
#             buildings_gdf = gdf[gdf['building'].notna()]
#         else:
#             buildings_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         if 'leisure' in gdf.columns:
#             parks_gdf = gdf[gdf['leisure'] == 'park']
#         else:
#             parks_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         if 'natural' in gdf.columns:
#             water_gdf = gdf[gdf['natural'] == 'water']
#         else:
#             water_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

#         result = {
#             "buildings_json": buildings_gdf.to_json(),
#             "parks_json": parks_gdf.to_json(),
#             "water_json": water_gdf.to_json(),
#         }

#         # --- CACHING LOGIC START ---
#         # Save the result to the cache file before returning
#         with open(cache_path, 'w') as f:
#             json.dump(result, f)
#         print(f"  [Tool Action] Saved new data to cache: {cache_path}")
#         # --- CACHING LOGIC END ---

#         return result
#     except Exception as e:
#         return {"error": f"An unexpected error occurred in fetch_geospatial_data: {e}"}


# def analyze_feasibility_metrics(road_line_json: str, buildings_json: str, parks_json: str, water_json: str) -> Dict[str, Any]:
#     """
#     Analyzes cost, social impact, and opportunity for a proposed road.
#     Use this tool as the main analysis step AFTER fetching geospatial data.
#     """
#     try:
#         road_line_gdf = gpd.read_file(road_line_json, driver='GeoJSON')
#         buildings_gdf = gpd.read_file(buildings_json, driver='GeoJSON')
#         parks_gdf = gpd.read_file(parks_json, driver='GeoJSON')
#         water_gdf = gpd.read_file(water_json, driver='GeoJSON')
        
#         road_line_m = road_line_gdf.to_crs("EPSG:3857").iloc[0].geometry
#         water_m = water_gdf.to_crs("EPSG:3857")
#         parks_m = parks_gdf.to_crs("EPSG:3857")

#         # Cost Analysis
#         length_km = road_line_m.length / 1000
#         base_cost = length_km * 5_000_000
#         bridge_length_m = 0
#         if not water_m.empty:
#             water_crossings = water_m.intersection(road_line_m)
#             bridge_length_m = sum(g.length for g in water_crossings if not g.is_empty)
#         bridge_cost = bridge_length_m * 25_000
#         total_cost = base_cost + bridge_cost

#         # Social Impact
#         num_buildings_impacted = 0
#         if not buildings_gdf.empty:
#             intersected_buildings = buildings_gdf[buildings_gdf.intersects(road_line_gdf.iloc[0].geometry)]
#             num_buildings_impacted = len(intersected_buildings)
        
#         # Environmental Impact
#         park_area_impacted_sqm = 0
#         if not parks_m.empty:
#             park_crossings = parks_m.intersection(road_line_m)
#             park_area_impacted_sqm = sum(g.area for g in park_crossings if not g.is_empty)

#         return {
#             "status": "Success",
#             "estimated_cost": f"${total_cost:,.0f}",
#             "road_length_km": f"{length_km:.2f}",
#             "social_impact": f"{num_buildings_impacted} buildings directly impacted.",
#             "environmental_impact": f"{park_area_impacted_sqm:,.0f} sq. meters of parkland impacted."
#         }
#     except Exception as e:
#         return {"error": f"An error occurred during analysis: {e}"}









# tools.py (Upgraded with State Management)

import os
import traceback
import googlemaps
import hashlib
import json
from typing import Dict, Any

from shapely.geometry import LineString
import osmnx as ox
import geopandas as gpd

# >>> NEW: Import ToolContext to access session state
from google.adk.tools import ToolContext

# Initialize the Google Maps client from the environment variable
gmaps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))


# --- Foundational Tool ---
def get_coordinates_from_placename(place_name: str) -> str:
    """Finds the geographic coordinates (latitude, longitude) for a given place name."""
    try:
        geocode_result = gmaps.geocode(place_name)
        if not geocode_result:
            return f"Could not find coordinates for {place_name}."
        
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return f"Coordinates: (lat={lat}, lon={lng})"
    except Exception as e:
        return f"An error occurred while geocoding: {e}"


# <<< NEW HELPER FUNCTION TO CLEAN DATA BEFORE SAVING >>>
def _clean_and_serialize_gdf(gdf: gpd.GeoDataFrame) -> str:
    """
    Selects useful columns, converts all property values to strings to prevent
    serialization errors, and then converts the GeoDataFrame to a JSON string.
    """
    # Define a whitelist of columns we want to keep. We only need a few.
    # We can easily add more here in the future if the agent needs them.
    SAFE_PROPERTIES = ['name', 'building', 'natural', 'leisure', 'water']
    
    # Start with just the essential geometry column
    columns_to_keep = ['geometry']
    
    # Add any of our safe properties that actually exist in this GeoDataFrame
    for prop in SAFE_PROPERTIES:
        if prop in gdf.columns:
            columns_to_keep.append(prop)
            
    # Create a new GeoDataFrame with only the columns we want
    clean_gdf = gdf[columns_to_keep].copy()

    # Now, for every property column we kept, convert all its values to strings.
    # This sanitizes messy data like dates, lists, or other objects into a safe format.
    for prop in SAFE_PROPERTIES:
        if prop in clean_gdf.columns:
            clean_gdf[prop] = clean_gdf[prop].astype(str)

    return clean_gdf.to_json()

    
# --- Geospatial Data Fetching Tool (Now returns data directly) ---
def fetch_geospatial_data(tool_context: ToolContext, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
    """
    Fetches geospatial data (buildings, parks, water) along a straight line corridor.
    This tool now returns the data directly instead of caching to a file.
    """
    print("  [Tool Action] Fetching data from OpenStreetMap API...")
    try:
        line_wgs84 = LineString([(start_lon, start_lat), (end_lon, end_lat)])
        print("  [Tool Action] Line constructed")
        
        # <<< NEW: Create a JSON representation of the road line to be saved to state
        road_line_json = gpd.GeoDataFrame([{'geometry': line_wgs84}], crs="EPSG:4326").to_json()
        print("  [Tool Action] Got the road line JSON")
        
        gdf_utm = gpd.GeoDataFrame.from_features(json.loads(road_line_json)).set_crs("EPSG:4326").to_crs("EPSG:3857")
        buffer_utm = gdf_utm.buffer(200).iloc[0]
        print("  [Tool Action] Added the buffer")

        buffer_utm_gs = gpd.GeoSeries([buffer_utm], crs="EPSG:3857")
        buffer_wgs84_gs = buffer_utm_gs.to_crs("EPSG:4326")
        buffer_wgs84_polygon = buffer_wgs84_gs.iloc[0]
        print("  [Tool Action] Got the polygon for road with buffer")

        tags = {"building": True, "natural": "water", "leisure": "park"}
        gdf = ox.features.features_from_polygon(buffer_wgs84_polygon, tags)
        print("  [Tool Action] Got the features from polygon")
        
        buildings_gdf = gdf[gdf['building'].notna()] if 'building' in gdf.columns else gpd.GeoDataFrame(geometry=[], crs=gdf.crs)
        parks_gdf = gdf[gdf['leisure'] == 'park'] if 'leisure' in gdf.columns else gpd.GeoDataFrame(geometry=[], crs=gdf.crs)
        water_gdf = gdf[gdf['natural'] == 'water'] if 'natural' in gdf.columns else gpd.GeoDataFrame(geometry=[], crs=gdf.crs)
        
        buildings_gdf.reset_index(inplace=True)
        parks_gdf.reset_index(inplace=True)
        water_gdf.reset_index(inplace=True)

        buildings_json = _clean_and_serialize_gdf(buildings_gdf)
        parks_json = _clean_and_serialize_gdf(parks_gdf)
        water_json = _clean_and_serialize_gdf(water_gdf)

        print("  [Tool Action] Saving fetched data to session state...")
        tool_context.state['road_line_json'] = road_line_json
        tool_context.state['buildings_json'] = buildings_json
        tool_context.state['parks_json'] = parks_json
        tool_context.state['water_json'] = water_json
        
        print("  [Tool Action] Got different feature details. Returning now...")

        return {
            "road_line_json": road_line_json,
            "buildings_json": buildings_json,
            "parks_json": parks_json,
            "water_json": water_json,
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred in fetch_geospatial_data: {e}"}

# # --- NEW TOOL: Save Data to State ---
# def save_data_to_state(tool_context: ToolContext, road_line_json: str, buildings_json: str, parks_json: str, water_json: str) -> str:
#     """
#     Saves the fetched geospatial data strings into the agent's session state.
#     Use this immediately after fetching data to store it for the analysis step.
    
#     Args:
#         tool_context (ToolContext): The context object providing access to session state.
#         road_line_json (str): JSON string of the road geometry.
#         buildings_json (str): JSON string of the building data.
#         parks_json (str): JSON string of the park data.
#         water_json (str): JSON string of the water data.

#     Returns:
#         str: A confirmation message.
#     """
#     print("  [Tool Action] Saving fetched data to session state...")
#     tool_context.state['road_line_json'] = road_line_json
#     tool_context.state['buildings_json'] = buildings_json
#     tool_context.state['parks_json'] = parks_json
#     tool_context.state['water_json'] = water_json
#     return "Geospatial data successfully saved to session state."



# def _gdf_from_geojson_str(s: str, crs="EPSG:4326") -> gpd.GeoDataFrame:
#     obj = json.loads(s)                      # validate JSON

#     for fidx, feat in enumerate(obj['features']):
#         if 'geometry' not in feat:
#             obj['features'][fidx]['geometry'] = None
    
#     if len(obj['features']) == 0:
#         obj['features'].append({'geometry': None})

#     try:
#         gdf = gpd.GeoDataFrame.from_features(obj, crs=crs)
#     except Exception as e:
#         print(f"Error: {e}")
#         import traceback
#         traceback.print_exc()

#         breakpoint()
    
#     return gdf

# In tools.py

def _gdf_from_geojson_str(s: str, crs="EPSG:4326") -> gpd.GeoDataFrame:
    """
    Robustly creates a GeoDataFrame from a GeoJSON string, handling empty feature collections.
    """
    try:
        obj = json.loads(s) # Validate and parse the JSON string
        
        # Safely get the list of features
        features = obj.get('features', [])
        
        # Create the GeoDataFrame from the list of features
        gdf = gpd.GeoDataFrame.from_features(features, crs=crs)
        
        # If the original GeoDataFrame was empty, from_features creates a GDF
        # with a geometry column of `None`. We ensure it's a proper empty GDF.
        if gdf.empty:
            # Ensure a 'geometry' column exists even if there are no features
            if 'geometry' not in gdf.columns:
                 gdf['geometry'] = None
            gdf.set_geometry('geometry', crs=crs, inplace=True)

        return gdf
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing GeoJSON string: {e}. Returning empty GeoDataFrame.")
        # Return a valid, empty GeoDataFrame on failure
        return gpd.GeoDataFrame(geometry=[], crs=crs)


# --- UPDATED TOOL: Analyze Metrics from State ---
def analyze_feasibility_metrics_from_state(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Analyzes feasibility by LOADING data from the session state.
    Use this tool as the final step after data has been fetched and saved to state.

    Args:
        tool_context (ToolContext): The context object providing access to session state.

    Returns:
        Dict[str, Any]: A dictionary containing a full quantitative analysis.
    """
    print("  [Tool Action] Loading data from session state for analysis...")
    # breakpoint()
    try:
        # Load all required data from the state
        road_line_json = tool_context.state.get('road_line_json')
        buildings_json = tool_context.state.get('buildings_json')
        parks_json = tool_context.state.get('parks_json')
        water_json = tool_context.state.get('water_json')

        if not all([road_line_json, buildings_json, parks_json, water_json]):
            return {"error": "Could not find all required geospatial data in the session state."}

        # The rest of the function is the same as before
        # road_line_gdf = gpd.read_file(road_line_json) #, driver='GeoJSON')
        # buildings_gdf = gpd.read_file(buildings_json) #, driver='GeoJSON')
        # parks_gdf = gpd.read_file(parks_json) #, driver='GeoJSON')
        # water_gdf = gpd.read_file(water_json) #, driver='GeoJSON')

        road_line_gdf = _gdf_from_geojson_str(road_line_json)
        buildings_gdf = _gdf_from_geojson_str(buildings_json)
        parks_gdf = _gdf_from_geojson_str(parks_json)
        water_gdf = _gdf_from_geojson_str(water_json)
        
        road_line_m = road_line_gdf.to_crs("EPSG:3857").iloc[0].geometry
        water_m = water_gdf.to_crs("EPSG:3857")
        parks_m = parks_gdf.to_crs("EPSG:3857")

        length_km = road_line_m.length / 1000
        base_cost = length_km * 5_000_000
        bridge_length_m = 0
        if not water_m.empty:
            water_crossings = water_m.intersection(road_line_m)
            bridge_length_m = sum(g.length for g in water_crossings if not g.is_empty)
        bridge_cost = bridge_length_m * 25_000
        total_cost = base_cost + bridge_cost

        num_buildings_impacted = 0
        if not buildings_gdf.empty:
            intersected_buildings = buildings_gdf[buildings_gdf.intersects(road_line_gdf.iloc[0].geometry)]
            num_buildings_impacted = len(intersected_buildings)
        
        park_area_impacted_sqm = 0
        if not parks_m.empty:
            park_crossings = parks_m.intersection(road_line_m)
            park_area_impacted_sqm = sum(g.area for g in park_crossings if not g.is_empty)

        analysis_report = {
            "status": "Success",
            "estimated_cost": f"${total_cost:,.0f}",
            "road_length_km": f"{length_km:.2f}",
            "social_impact": f"{num_buildings_impacted} buildings directly impacted.",
            "environmental_impact": f"{park_area_impacted_sqm:,.0f} sq. meters of parkland impacted."
        }

        print(f"{analysis_report = }")

        return analysis_report

    except Exception as e:
        traceback.print_exc()
        breakpoint()
        return {"error": f"An error occurred during analysis: {e}"}
