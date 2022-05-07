import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import json

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

uploaded_file = st.sidebar.file_uploader(label="Upload GeoJSON file", type=['geojson'], accept_multiple_files=False)

col1, col2 = st.columns(2)

with col1:
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        lon  = data['features'][0]['geometry']['coordinates'][0][0][0]
        lat  = data['features'][0]['geometry']['coordinates'][0][0][1]
        st.pydeck_chart(pdk.Deck(
            map_provider="mapbox",
            map_style=pdk.map_styles.SATELLITE,
            api_keys  = { "mapbox": "pk.eyJ1IjoiZ3JvbDIwMjAiLCJhIjoiY2tvajI0MW5pMDMxMDJ3bzdpN3dzbHBidyJ9.jxYSuCXT1u1eFKMMWwSFVg"},
            initial_view_state=pdk.ViewState(
                latitude  = lat,
                longitude = lon,
                zoom=12,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'GeoJsonLayer',
                    data=data,
                    get_fill_color=[0, 0, 0]
                ),
            ],
        ))
        st.write()