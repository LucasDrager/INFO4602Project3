from flask import Flask, render_template
import altair as alt
import pandas as pd
import geopandas as gpd
import os

app = Flask(__name__)

###LOADING GRAPH DATA
merged_data2 = gpd.read_file('./Data/graphDataSets/Lucas.geojson')
merged_data = gpd.read_file('./Data/graphDataSets/Will.geojson')
gdf = gpd.read_file('./Data/graphDataSets/Emelia.geojson')
### OUR GRAPH CODE

min_pm25 = merged_data2['pm25_concentration'].min()
max_pm25 = merged_data2['pm25_concentration'].max()

# Create a slider selection
slider = alt.binding_range(min=2010, max=2022, step=1, name="Year")
year_selection = alt.selection_point(fields=['year'], bind=slider, name="Select")

# Create the chart
chart1 = alt.Chart(merged_data2).mark_geoshape(
    stroke='white',        # Set the border color (e.g., black)
    strokeWidth=0.4
).encode(
    color=alt.condition(
        alt.datum.pm25_concentration > 0,
        alt.Color(
            'pm25_concentration:Q',
            title='PM2.5 Concentration',
            scale=alt.Scale(domain=[min_pm25, max_pm25], clamp=True, scheme='magma',reverse=True)
        ),
        alt.value('lightgray')  # Gray out countries with PM2.5 = 0
    ),
    tooltip=[
        alt.Tooltip('country_name:N', title='Country'),
        alt.Tooltip('pm10_concentration:Q', title='PM10'),
        alt.Tooltip('pm25_concentration:Q', title='PM2.5'),
        alt.Tooltip('no2_concentration:Q', title='NO2')
    ]
).properties(
    width=800,
    height=600,
    title="Chemical Concentrations in Europe"
).project(
    type='mercator',
    center=[10, 50],
    scale=500
).add_params(
    year_selection
).transform_filter(
    year_selection
)

# Create the chart
chart2 = alt.Chart(merged_data2).mark_geoshape(
    stroke='white',        # Set the border color (e.g., black)
    strokeWidth=0.4
).encode(
    color=alt.condition(
        alt.datum.pm25_concentration > 0,
        alt.Color(
            'pm10_concentration:Q',
            title='PM1.0 Concentration',
            scale=alt.Scale(domain=[min_pm25, max_pm25], clamp=True, scheme='magma',reverse=True)
        ),
        alt.value('lightgray')  # Gray out countries with PM2.5 = 0
    ),
    tooltip=[
        alt.Tooltip('country_name:N', title='Country'),
        alt.Tooltip('pm10_concentration:Q', title='PM10'),
        alt.Tooltip('pm25_concentration:Q', title='PM2.5'),
        alt.Tooltip('no2_concentration:Q', title='NO2')
    ]
).properties(
    width=800,
    height=600,
    title="Chemical Concentrations in Europe"
).project(
    type='mercator',
    center=[10, 50],
    scale=500
).add_params(
    year_selection
).transform_filter(
    year_selection
)

# Create the chart
chart3 = alt.Chart(merged_data2).mark_geoshape(
    stroke='white',        # Set the border color (e.g., black)
    strokeWidth=0.4
).encode(
    color=alt.condition(
        alt.datum.no2_concentration > 0,
        alt.Color(
            'no2_concentration:Q',
            title='NO2 Concentration',
            scale=alt.Scale(domain=[min_pm25, max_pm25], clamp=True, scheme='magma',reverse=True)
        ),
        alt.value('lightgray')  # Gray out countries with PM2.5 = 0
    ),
    tooltip=[
        alt.Tooltip('country_name:N', title='Country'),
        alt.Tooltip('pm10_concentration:Q', title='PM10'),
        alt.Tooltip('pm25_concentration:Q', title='PM2.5'),
        alt.Tooltip('no2_concentration:Q', title='NO2')
    ]
).properties(
    width=800,
    height=600,
    title="Chemical Concentrations in Europe"
).project(
    type='mercator',
    center=[10, 50],
    scale=500
).add_params(
    year_selection
).transform_filter(
    year_selection
)


merged_data["Lives Lost per Person"] = merged_data["Years Of Life Lost"] / merged_data["Population"]

choropleth = alt.Chart(merged_data).mark_geoshape(
    stroke='white', strokeWidth=0.5
).encode(
    color=alt.Color(
        "Premature Deaths:Q",
        scale=alt.Scale(scheme="reds"),
        title="Premature Deaths",
        legend=alt.Legend(title="Premature Deaths", orient="bottom-right")
    ),
    tooltip=[
        alt.Tooltip("NAME:N", title="Country"),
        alt.Tooltip("Premature Deaths:Q", title="Premature Deaths", format=",.0f"),
        alt.Tooltip("Years Of Life Lost:Q", title="Years of Life Lost", format=",.0f"),
        alt.Tooltip("Lives Lost per Person:Q", title="Lives Lost per Person", format=".6f")
    ]
).project(
    type="mercator",
    scale=600,
    center=[10, 50]
).properties(
    width=1000,
    height=700,
    title=alt.TitleParams(
        "Premature Deaths and Lives Lost per Person in Europe",
        fontSize=20,
        fontWeight="bold",
        anchor="middle"
    )
).configure_view(
    stroke=None
).configure_legend(
    titleFontSize=14,
    labelFontSize=12,
    gradientLength=200
)

import altair as alt

hover_selection = alt.selection_point (
    fields=['country_name'],
    on='mouseover',
    nearest=True,
    empty='none'
)

scatter = alt.Chart(gdf).mark_circle(size=100).encode(
    x='pm25_concentration:Q',
    y='resp_disease:Q',
    size=alt.Size('respCases_Deaths:Q', scale=alt.Scale(range=[10, 1000])),
    color=alt.condition(
        hover_selection, alt.value('steelblue'),alt.value('lightgray')
    ),
    tooltip=['country_name', 'pm25_concentration', 'resp_disease']
).add_params (
    hover_selection
).properties(
    title="Scatter Plot of PM2.5 vs VALUE",
    width=400,
    height=300
)

map_chart = alt.Chart(gdf).mark_geoshape(
    stroke='white'
).encode(
    color=alt.condition(
        hover_selection,
        alt.value('steelblue'),
        alt.value('lightgray')
    ),
    tooltip=['country_name', 'resp_disease']
).properties(
    title="Map of Countries in Europe",
    width=500,
    height=400
).project(
    type='mercator',
    center=[10, 50],
)

# combing da two
combined_chart = (scatter | map_chart).resolve_scale(
    color='shared'
)

# chart1.save('./static/charts/chart1.json',format='json')
chart2.save('./static/charts/chart2.json',format='json')
chart3.save('./static/charts/chart3.json',format='json')
choropleth.save('./static/charts/chart4.json',format='json')
combined_chart.save('./static/charts/chart5.json',format='json')

###WEBSITE CODE

@app.route('/')
def index():
    # Load all charts
    count = 0
    return render_template('Index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
