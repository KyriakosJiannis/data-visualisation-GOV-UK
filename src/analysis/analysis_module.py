import re
import os
import pandas as pd
import requests
import glob
import io
import geopandas as gpd
import matplotlib as mpl

mpl.use('TkAgg', force=True)
print("Switched to:", mpl.get_backend())

import matplotlib.pyplot as plt
import seaborn as sns
from zipfile import ZipFile


def load_nomis_data(nomis_csv_url: str) -> pd.DataFrame:
    """
    Load open data from a CSV file located at the given URL and return it as a Pandas DataFrame.

    :param nomis_csv_url: The URL of the CSV file containing open data.
    :return: A Pandas DataFrame containing the loaded open data.
    """
    return pd.read_csv(nomis_csv_url)


def load_opendatasoft_shapefiles(zip_url: str) -> gpd.GeoDataFrame:
    """
    Load shapefiles from a given URL, extract, and return a GeoPandas DataFrame.

    :param zip_url: URL of the zipped shapefiles.
    :return: GeoPandas DataFrame.
    """
    # Download and extract the zip file
    with requests.get(zip_url) as response:
        with ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()

    # Read the shapefile into a GeoPandas DataFrame
    shapefile_name = zip_url.split("/")[-1].replace("zip", "shp")
    df_map = gpd.read_file(shapefile_name)

    # Remove temporary files
    temporary_files = glob.glob(f'./{shapefile_name.replace("shp", "*")}')
    for filename in temporary_files:
        os.remove(filename)

    return df_map


def combine_nomis_and_geo_data(nomis_data: pd.DataFrame, geo_data: gpd.GeoDataFrame, nomis_key: str,
                               geo_key: str) -> gpd.GeoDataFrame:
    """
    Combine Nomis and Geo Data.

    Parameters:
    :param nomis_data: Nomis Data (Pandas DataFrame).
    :param geo_data: Geo Data (GeoPandas DataFrame).
    :param nomis_key: Key for Nomis Data.
    :param geo_key: Key for Geo Data.

    :return: Combined GeoPandas DataFrame.
    """

    # Delete rows containing pattern All Categories
    pattern = re.compile(r'All categories:', flags=re.IGNORECASE)
    nomis_data = nomis_data[~nomis_data['C_RELPUK11_NAME'].str.contains(pattern)]

    # Combine shapefile with nomis
    merged_gdf = geo_data.set_index(geo_key).join(nomis_data.set_index(nomis_key)).reset_index()

    return merged_gdf


def load_data_and_merge(nomis_csv_url: str, opendatasoft_geo_zip_url: str, nomis_key: str, geo_key: str) -> gpd.GeoDataFrame:
    """
    Load Nomis data, OpenDataSoft geospatial data, and merge them based on specified keys.

    Parameters:
    :param nomis_csv_url: The URL of the Nomis CSV file.
    :param opendatasoft_geo_zip_url: The URL of the OpenDataSoft geospatial data in ZIP format.
    :param nomis_key: The key to merge Nomis data on.
    :param geo_key: The key to merge geospatial data on.

    Returns:
    :return: A GeoDataFrame containing the merged data.
    """

    nomis_data = load_nomis_data(nomis_csv_url)

    opendatasoft_gdf = load_opendatasoft_shapefiles(opendatasoft_geo_zip_url)

    merged_gdf = combine_nomis_and_geo_data(nomis_data, opendatasoft_gdf, nomis_key, geo_key)

    return merged_gdf


def subset_religion_gdf(in_gdf: gpd.GeoDataFrame, religion: str) -> gpd.GeoDataFrame:
    """
    Subset a GeoDataFrame at the religion level and sort by OBS_VALUE in descending order.

    :param in_gdf: Input GeoDataFrame to be subset.
    :param religion: The name of the religion for subsetting.

    :return: A subset of the input GeoDataFrame filtered by the specified religion,
             sorted by OBS_VALUE in descending order.
    """
    subset_gdf = in_gdf[in_gdf['C_RELPUK11_NAME'] == religion].copy()
    subset_gdf.sort_values(by='OBS_VALUE', axis=0, ascending=False, inplace=True)

    return subset_gdf


def plot_nomis_data(geo_data: gpd.GeoDataFrame, cmap='winter', title='', barchart=None, save_path=None) -> plt.Axes:
    """
    Plot Nomis data on a map and optionally as a bar chart.

    :param geo_data: GeoPandas DataFrame containing Nomis data and geometries.
    :param cmap: Colormap for the map and bar chart.
    :param title: Title for the plot.
    :param barchart: If True, include a bar chart alongside the map.
    :param save_path: If provided, save the plot to the specified path. If None, display the plot.

    :return: Matplotlib plot object.
    """
    if barchart:
        # Map of the UK and Bar Chart

        # Set the style to white
        sns.set_style("white")

        # Create a subplot with two axes
        fig, axes = plt.subplots(1, 2, figsize=(15, 7), constrained_layout=True)
        fig.suptitle(title, fontsize=16)

        # Plot the map on the first axis
        axes[0] = geo_data.plot(column="OBS_VALUE", cmap=cmap, linewidth=0.2, edgecolor='grey', ax=axes[0], legend=True)
        axes[0].axis("off")

        # Plot the bar chart on the second axis
        axes[1] = sns.barplot(x="OBS_VALUE",
                              y='GEOGRAPHY_NAME',
                              data=geo_data,
                              palette=mpl.cm.ScalarMappable(cmap=cmap).to_rgba(geo_data["OBS_VALUE"]))

        # Customize the bar chart
        axes[1].set_ylabel('')
        axes[1].set_xlabel('')
        axes[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        # Add percentage labels to the bar chart
        for i in axes[1].patches:
            axes[1].text(i.get_width() + .5, i.get_y() + .45,
                         str(round((i.get_width()), 2)) + '%', fontsize=12, color='black')
    else:
        # Map of the UK based on NomisR values

        # Create a single-axis subplot
        fig, axes = plt.subplots(1, figsize=(10, 6))
        fig.suptitle(title, fontsize=16)

        # Plot the map on the single axis
        axes = geo_data.plot(column="OBS_VALUE", cmap=cmap, linewidth=0.2, edgecolor='grey', ax=axes, legend=True)
        axes.axis("off")

    # Save or show the plot
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show()

    # Return the matplotlib plot object
    return axes
