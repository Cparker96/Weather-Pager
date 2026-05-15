import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from logger.logger import logger
from io import BytesIO

def check_if_subscribed(states: list[str], events: list[str], latest_event: dict):
    if_subscribed_state = False
    if_subscribed_event = False

    for state in states:
        if state in latest_event["title"]:
            if_subscribed_state = True
            break
    
    for event in events:
        if event in latest_event["categories"]["id"]:
            if_subscribed_event = True
            break

    return if_subscribed_state, if_subscribed_event


def pack_metadata(latest_event: dict, image: BytesIO) -> dict:
    event_metadata = {}

    event_metadata.update(
        {"Date": latest_event["geometry"][0]["date"],
         "Title": latest_event["title"],
         "Area": latest_event["geometry"][0]["magnitudeValue"],
         "Image": image
        }
    )

    return event_metadata


def plot_coordinates(latest_event: dict) -> BytesIO:
    # strip out state
    split_title = latest_event["title"].split(",")
    state = split_title[-1].strip()

    # pack into dataframe
    df = pd.DataFrame({
        'State': [state],
        'Longitude': [latest_event["geometry"][0]["coordinates"][0]],
        'Latitude': [latest_event["geometry"][0]["coordinates"][1]],
    })

    # plot onto map
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")

    states_gdf = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_20m.zip")
    counties_gdf = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_county_20m.zip")

    target_state = states_gdf[
        states_gdf["NAME"] == state
    ]

    state_fips = target_state.iloc[0]["STATEFP"]
    state_counties = counties_gdf[counties_gdf["STATEFP"] == state_fips]

    fig, ax = plt.subplots(figsize=(8, 8))

    target_state.plot(ax=ax, color="white", edgecolor="black")
    state_counties.plot(ax=ax, color="none", edgecolor="gray", linewidth=0.5)

    gdf.plot(ax=ax, color="red", markersize=100)
    ax.set_title(f"Weather Event - {state}")

    # open image buffer to pack bytes
    buffer = BytesIO()
    plt.savefig(buffer, dpi=300, bbox_inches="tight")

    plt.close(fig)

    buffer.seek(0)
    
    return buffer