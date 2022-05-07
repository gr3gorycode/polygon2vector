import streamlit as st
import pandas as pd
import plotly.express as px
import pygeohash as pgh
from datetime import datetime

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")
# Data paths and Keys
px.set_mapbox_access_token("pk.eyJ1IjoiZ3JvbDIwMjAiLCJhIjoiY2tvajI0MW5pMDMxMDJ3bzdpN3dzbHBidyJ9.jxYSuCXT1u1eFKMMWwSFVg")
DF_PIXEL = "https://github.com/aadi350/grd_2022/raw/main/res/df_pixel.parquet"
DF_PIXEL2 = "https://github.com/aadi350/grd_2022/raw/main/res/pred_21_24.parquet"

st.title('2022 GRD AI Data Challenge')


@st.cache
def load_data(path_url:str) -> pd.DataFrame:
    df = pd.read_parquet(path_url)
    return df


data_load_state = st.text('Loading data...')
data = load_data(DF_PIXEL)
data_load_state.text("Done! (using st.cache)")

data2_load_state = st.text('Loading data...')
data2 = load_data(DF_PIXEL2).reset_index().rename(columns={'index':'date'})
data2_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data', key="Check1"):
    st.subheader('Raw data')
    st.write(data.head(10))

map_data = data[(data.date == datetime(2000, 9, 1)) | (data.date == datetime(2019, 9, 1))]
map_data = map_data.melt(id_vars='date', value_name="water_temp_2")
map_data['lat'] = map_data.variable.apply(lambda x: pgh.decode(x)[0])
map_data['lon'] = map_data.variable.apply(lambda x: pgh.decode(x)[1])

col1_1, col1_2 = st.columns((1,1))
with col1_1:
    fig = px.scatter_mapbox(map_data[map_data.date == datetime(2000, 9, 1)], lat="lat", lon="lon", color="water_temp_2",
                            color_continuous_scale=px.colors.diverging.RdBu_r, size_max=15, zoom=4.2,
                            color_continuous_midpoint=28)
    fig.update_layout(title="Measured Sea Water Temperature at 2m in the East Caribbean (September 2000)")
    fig.update_traces(marker_cmax= 36)
    st.plotly_chart(fig)

with col1_2:
    fig = px.scatter_mapbox(map_data[map_data.date == datetime(2019, 9, 1)], lat="lat", lon="lon", color="water_temp_2",
                            color_continuous_scale=px.colors.diverging.RdBu_r, size_max=15, zoom=4.2,
                            color_continuous_midpoint=28)
    fig.update_layout(title="Measured Sea Water Temperature at 2m in the East Caribbean (September 2019)")
    st.plotly_chart(fig)



col2_1, col2_2 = st.columns((1,1))
cols_to_plot = [x for x in data.columns if x != "date"][:10]+['date']
with col2_1:
    DD = data[cols_to_plot].melt(id_vars='date', var_name='geohash', value_name='water_temp_2')
    fig = px.line(DD[DD.date < datetime(2021,1,1)], x="date", y="water_temp_2", color='geohash',
                  title='Measured Sea Water Temperature at 2m in the East Caribbean (Year 2000-2021)')
    fig.update_layout(yaxis_title="Sea Water Temperature 2m (Celsius)")
    # fig.show()
    st.plotly_chart(fig)

with col2_2:
    DD = data2[cols_to_plot].melt(id_vars='date', var_name='geohash', value_name='water_temp_2')
    DD['water_temp_2'] = DD.water_temp_2.apply(lambda x: x*5.644704 + 25.0451290)
    fig = px.line(DD[DD.date >= datetime(2021,1,1)], x="date", y="water_temp_2", color='geohash',
                  title='Predicted Sea Water Temperature at 2m in the East Caribbean (Year 2022-2024)')
    fig.update_layout(yaxis_title="Sea Water Temperature 2m (Celsius)")
    # fig.show()
    st.plotly_chart(fig)

col3_1, col3_2 = st.columns((2,1))
with col3_1:
    DD1 = data2[cols_to_plot].melt(id_vars='date', var_name='geohash', value_name='water_temp_2')
    DD1['water_temp_2'] = DD1.water_temp_2.apply(lambda x: x*5.644704 + 25.0451290)
    DD = data[cols_to_plot].melt(id_vars='date', var_name='geohash', value_name='water_temp_2')
    DD1['type'] = "Predicted"
    DD['type'] = "Measured"
    DD3 = pd.concat([DD[DD.date <= datetime(2021,1,1)], DD1[DD1.date >= datetime(2021,1,1)]], ignore_index=True)
    fig = px.line(DD3.sort_values(by='date'), x="date", y="water_temp_2", color='type',
                  title='Sea Water Temperature at 2m in the East Caribbean (Year 2000-2024)')
    fig.update_layout(yaxis_title="Sea Water Temperature 2m (Celsius)")
        # fig.show()
    st.plotly_chart(fig, use_container_width=True)