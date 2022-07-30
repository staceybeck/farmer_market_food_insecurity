#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project:     Desktop
# @Filename:    folium_choropleth.py
# @IDE:         PyCharm

# Import libraries
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import os



def choropleth(df, quantitative_value, values_to_show, key, hovertext, fields, legend_text):
    """

    :param df                   :  dataframe
    :param quantitative_value   :  string of quant variable to show
    :param values_to_show       :  array of fields to display, use for map
    :param key                  :  string for column by which to show (STATE, COUNTY)
    :param hovertext            :  array of string text to display in hovertext
    :param fields               :  array of column names to display in hovertext
    :param legend_text          :  string for legend title display
    :return                     :  first layer and the base map
    """


    # Center the map
    lat = 40.116386
    long_ = -101.299591

    state_map = folium.Map(location=[lat, long_], zoom_start=3.8, tiles=None)
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(state_map)

    scale = (df[quantitative_value].quantile((0, 0.1, 0.75, 0.9, 0.98, 1))).tolist()
    state_map.choropleth(
        geo_data=df,
        name='Choropleth',
        data=df,
        columns=values_to_show,
        key_on=f"feature.properties.{key}",
        fill_color='YlGnBu',
        threshold_scale=scale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name=legend_text,
        smooth_factor=0
    )

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}
    layer1 = folium.features.GeoJson(
        df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=fields,
            aliases=hovertext,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    return layer1, state_map

if __name__ == "__main__":
    path = 'data/'
    dir_list = os.listdir(path)
    for f in dir_list:
        if f == 'dataframe.geojson':
            file = f

    df = gpd.read_file(path + file) # Needs to be a geopandas DF with one geometry datatype
    state_df = gpd.GeoDataFrame(data, geometry='geometry')
    quantitative_value = 'Percent Markets'
    values_to_show = ['STATE','Percent Markets']
    key = 'STATE'
    hovertext = ['STATE: ',"Number of Farmers' Markets, CSA, and On Markets %: "]
    fields = ['State_name','Percent Markets']
    legend_text = 'Data in %'

    layer1, state_map = choropleth(state_df,
                                   quantitative_value,
                                   values_to_show,
                                   key,
                                   hovertext,
                                   fields,
                                   legend_text)
    state_map.add_child(layer1)
    state_map.keep_in_front(layer1)
    folium.LayerControl().add_to(state_map)
    state_map
