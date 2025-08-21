# tools.py
# This file contains the specialized "tools" the agent can use.
# VERSION 7: Fixes the KeyError by ensuring analyze_cost returns all required data points.

import osmnx as ox
import geopandas as gpd
from shapely.geometry import LineString
import folium

# --- Tool 1: Geospatial Data Fetcher (Efficient & Modern Version) ---
def fetch_geospatial_data(point_a, point_b):
    """
    Fetches map data only within a narrow corridor around the line between two points,
    using modern, standard GeoPandas methods for projection.
    """
    try:
        line_wgs84 = LineString([point_a[::-1], point_b[::-1]])
        gdf_wgs84 = gpd.GeoDataFrame([{'geometry': line_wgs84}], crs="EPSG:4326")
        
        gdf_utm = gdf_wgs84.to_crs("EPSG:3857")
        buffer_utm = gdf_utm.buffer(500).iloc[0]

        buffer_utm_gs = gpd.GeoSeries([buffer_utm], crs="EPSG:3857")
        buffer_wgs84_gs = buffer_utm_gs.to_crs("EPSG:4326")
        buffer_wgs84_polygon = buffer_wgs84_gs.iloc[0]

        tags = {
            "building": True, 
            "natural": ["water", "wood"],
            "leisure": ["park", "nature_reserve"], 
            "amenity": ["hospital", "school", "marketplace"], 
            "shop": True,
        }
        
        gdf = ox.features.features_from_polygon(buffer_wgs84_polygon, tags)
        
        return {
            "buildings": gdf[gdf['building'].notna()],
            "water": gdf[gdf['natural'] == 'water'],
            "parks": gdf[gdf['leisure'].isin(['park', 'nature_reserve'])],
            "amenities": gdf[gdf['amenity'].notna() | gdf['shop'].notna()],
        }
    except Exception as e:
        print(f"Could not fetch data from OpenStreetMap. The area might be empty or an error occurred: {e}")
        return None

# --- Tool 2: Cost Analysis Tool ---
def analyze_cost(road_line_m, water_gdf_wgs84, parks_gdf_wgs84):
    """Analyzes construction cost and returns a detailed dictionary of all components."""
    COST_PER_KM = 1_000_000
    BRIDGE_COST_PER_METER = 10_000
    PARK_MITIGATION_COST_PER_METER = 5_000

    length_km = road_line_m.length / 1000
    base_cost = length_km * COST_PER_KM
    bridge_cost, park_cost = 0, 0
    bridge_length_m, park_crossing_length_m = 0, 0

    if not water_gdf_wgs84.empty:
        water_m = water_gdf_wgs84.to_crs("EPSG:3857")
        water_crossings = water_m.intersection(road_line_m)
        bridge_length_m = sum(geom.length for geom in water_crossings if not geom.is_empty)
        bridge_cost = bridge_length_m * BRIDGE_COST_PER_METER
    
    if not parks_gdf_wgs84.empty:
        parks_m = parks_gdf_wgs84.to_crs("EPSG:3857")
        park_crossings = parks_m.intersection(road_line_m)
        park_crossing_length_m = sum(geom.length for geom in park_crossings if not geom.is_empty)
        park_cost = park_crossing_length_m * PARK_MITIGATION_COST_PER_METER

    total_cost = base_cost + bridge_cost + park_cost
    
    # The function now returns a detailed dictionary with all the keys the report needs.
    return {
        "total_cost": total_cost,
        "base_cost": base_cost,
        "bridge_cost": bridge_cost,
        "park_cost": park_cost,
        "length_km": length_km,
        "bridge_length_m": bridge_length_m,
        "park_crossing_length_m": park_crossing_length_m
    }

# --- Tool 3: Social Impact Tool ---
def analyze_social_impact(road_line_wgs84, buildings_gdf_wgs84):
    """Analyzes social disruption by counting intersected buildings."""
    if buildings_gdf_wgs84.empty:
        return { "impact_score": 0, "num_buildings_intersected": 0, "intersected_buildings_gdf": buildings_gdf_wgs84 }

    intersected_buildings = buildings_gdf_wgs84[buildings_gdf_wgs84.intersects(road_line_wgs84)]
    num_buildings = len(intersected_buildings)
    impact_score = num_buildings * 10 
    
    return {
        "impact_score": impact_score, 
        "num_buildings_intersected": num_buildings,
        "intersected_buildings_gdf": intersected_buildings
    }

# --- Tool 4: Opportunity Analysis Tool ---
def analyze_opportunity(amenities_gdf):
    """Analyzes opportunity by counting amenities within the fetched corridor."""
    num_amenities = len(amenities_gdf)
    opportunity_score = num_amenities * 5
    
    return {
        "opportunity_score": opportunity_score, 
        "amenities_in_reach": num_amenities,
    }


# --- Tool 5: Report Generator Tool (Dashboard Version) ---
def generate_report(agent_memory):
    """
    Generates a final HTML dashboard report with a text summary on the left
    and an interactive map on the right.
    """
    point_a = agent_memory['inputs']['point_a']
    point_b = agent_memory['inputs']['point_b']
    cost_data = agent_memory['cost']
    social_data = agent_memory['social_impact']
    opportunity_data = agent_memory['opportunity']

    # Create map centered on the midpoint
    map_center = [(point_a[0] + point_b[0]) / 2, (point_a[1] + point_b[1]) / 2]
    m = folium.Map(
        location=map_center, 
        zoom_start=14, 
        # tiles="cartodbpositron",
    )

    # Add data layers to the map
    if not agent_memory['data']['parks'].empty:
        folium.GeoJson(agent_memory['data']['parks'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 1}, name="Parks").add_to(m)
    if not agent_memory['data']['water'].empty:
        folium.GeoJson(agent_memory['data']['water'], style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'weight': 1}, name="Water Bodies").add_to(m)
    
    # Highlight intersected buildings in red
    intersected_bldgs = social_data['intersected_buildings_gdf']
    if not intersected_bldgs.empty:
        folium.GeoJson(intersected_bldgs, style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'weight': 1}, tooltip="Displaced Building").add_to(m)

    # Highlight nearby amenities in purple
    nearby_amenities = agent_memory['data']['amenities']
    if not nearby_amenities.empty:
        folium.GeoJson(nearby_amenities, marker=folium.Marker(icon=folium.Icon(color='purple')), tooltip="New Opportunity").add_to(m)
        # for _, amenity in nearby_amenities.iterrows():
        #     location = [amenity.geometry.centroid.y, amenity.geometry.centroid.x]
        #     folium.Marker(location=location, icon=folium.Icon(color='purple', icon='info-sign'), tooltip="New Opportunity").add_to(m)

    # Add the proposed road line
    summary = f"""
    <b>Feasibility Report</b><br>
    --------------------------<br>
    <b>Estimated Cost:</b> ${agent_memory['cost']['total_cost']:,.0f}<br>
    <b>Social Impact Score:</b> {agent_memory['social_impact']['impact_score']} ({agent_memory['social_impact']['num_buildings_intersected']} buildings affected)<br>
    <b>Opportunity Score:</b> {agent_memory['opportunity']['opportunity_score']} ({agent_memory['opportunity']['amenities_in_reach']} amenities made accessible)<br>
    """
    folium.GeoJson(agent_memory['inputs']['road_line_wgs84'], style_function=lambda x: {'color': '#FF9800', 'weight': 5}, name="Proposed Road", tooltip=summary).add_to(m)
    
    # Add markers for start and end points
    folium.Marker(location=point_a, popup="Point A", icon=folium.Icon(color="green", icon='play')).add_to(m)
    folium.Marker(location=point_b, popup="Point B", icon=folium.Icon(color="red", icon='stop')).add_to(m)

    map_html = m._repr_html_()

    text_report_html = f"""
        <h2>Project Overview</h2>
        <p>This report provides a preliminary feasibility analysis for a proposed road link.</p>
        <ul>
            <li><b>Start Point (A):</b> {point_a}</li>
            <li><b>End Point (B):</b> {point_b}</li>
            <li><b>Total Length:</b> {cost_data['length_km']:.2f} km</li>
        </ul>

        <h2>Cost Analysis</h2>
        <p>The total estimated cost is calculated based on length and required infrastructure.</p>
        <table>
            <tr>
                <td>Base Construction Cost</td>
                <td>${cost_data['base_cost']:,.0f}</td>
            </tr>
            <tr>
                <td>Bridge Construction ({cost_data['bridge_length_m']:.0f}m)</td>
                <td>${cost_data['bridge_cost']:,.0f}</td>
            </tr>
            <tr>
                <td>Park Mitigation ({cost_data['park_crossing_length_m']:.0f}m)</td>
                <td>${cost_data['park_cost']:,.0f}</td>
            </tr>
            <tr class="total-row">
                <td><b>Total Estimated Cost</b></td>
                <td><b>${cost_data['total_cost']:,.0f}</b></td>
            </tr>
        </table>

        <h2>Social & Environmental Impact</h2>
        <p>This section assesses the potential disruption to local communities and protected areas.</p>
        <ul>
            <li><span class="metric-value">{social_data['num_buildings_intersected']}</span> buildings are directly on the proposed path, resulting in a high social impact.</li>
            <li>The route crosses <span class="metric-value">{cost_data['park_crossing_length_m']:.0f} meters</span> of parkland/nature reserves.</li>
        </ul>

        <h2>Economic Opportunity</h2>
        <p>The new link has the potential to improve access to local services and commerce.</p>
        <ul>
            <li>The proposed road provides new, direct access to <span class="metric-value">{opportunity_data['amenities_in_reach']}</span> key amenities (shops, schools, etc.).</li>
        </ul>

        <h2>Summary & Recommendation</h2>
        <p>
            The proposed route offers a significant <b>opportunity score ({opportunity_data['opportunity_score']})</b> by enhancing connectivity. However, this is offset by a very high 
            <b>social impact score ({social_data['impact_score']})</b> and a substantial <b>cost of ${cost_data['total_cost']:,.0f}</b>.
            Further investigation into alternative routes that avoid residential displacement is strongly recommended.
        </p>
    """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pathfinder Agent Feasibility Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
            .container {{ display: flex; flex-direction: row; height: 100vh; }}
            .column {{ padding: 20px; box-sizing: border-box; }}
            .text-column {{ width: 40%; overflow-y: auto; background-color: #ffffff; }}
            .map-column {{ width: 60%; }}
            h1, h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h1 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            td {{ padding: 8px 12px; border: 1px solid #ddd; }}
            .total-row td {{ background-color: #f2f2f2; font-weight: bold; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ background-color: #fafafa; margin-bottom: 8px; padding: 10px; border-left: 4px solid #FF9800; }}
            .metric-value {{ font-weight: bold; color: #333; }}
            .map-column .folium-map {{ width: 100%; height: 100%; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="column text-column">
                <h1>Feasibility Study</h1>
                {text_report_html}
            </div>
            <div class="column map-column">
                {map_html}
            </div>
        </div>
    </body>
    </html>
    """

    report_path = "feasibility_report.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return report_path