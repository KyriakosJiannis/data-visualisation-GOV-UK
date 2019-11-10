""" this script contains the data visualisation GOV UK modules"""


def loadShapefiles(zip_file_url):
    """download zip and load shp"""
    import requests, zipfile, io, os, glob
    import geopandas as gpd

    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    df_map = gpd.read_file(zip_file_url.split("/")[-1].replace("zip", "shp"))

    for filename in glob.glob(''.join(['./', zip_file_url.split("/")[-1].replace("zip", "*")])):
        os.remove(filename)
    return df_map


def plot_nomisr_shapefile(nomisr,
                          shapefile,
                          nomisrKey='GEOGRAPHY_CODE',
                          shapefilekey='',
                          subset='',
                          cmap="winter",
                          title="United Kingdom labour data",
                          tests="off",
                          barchart="off"):
    """
    function, which joins United Kingdom shapefiles with National Statistics data
    and create map for United Kingdom by its counties and colours based on specific measurement size values
        uses R API outputs to get the UK labour data, nomisr, https://cran.r-project.org/web/packages/nomisr/index.html
        UK shapefiles from https://public.opendatasoft.com

    Parameters
    ----------
    :param barchart: default off, prints barcharts
    :param tests: default off, print data tests and profiling
    :param title: Give a title in the chart
    :param cmap: cmap from Matplotlib https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    :param subset: rows selections
    :param shapefilekey: shapefile key variable
    :param nomisrKey:  nomis key variable
    :param shapefile: shapefile dataframe
    :param nomisr: nomis pandas dataframe
    :returns the UK map based on the selected Labour Market Data.
    """

    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib_venn import venn2
    import pandas_profiling

    # delete all rows total rows
    nomisr = nomisr.drop(nomisr[(nomisr.C_RELPUK11_NAME == "All categories: Religion")].index)

    # data set tests, venn diagram and profiling
    if tests != "off":
        '''profiling '''
        pandas_profiling.ProfileReport(nomisr)
        '''Venn diagram '''
        venn2([set(shapefile[shapefilekey]), set(nomisr[nomisrKey])])
        '''test the shapefile areas'''
        f1, ax1 = plt.subplots(1, figsize=(10, 10))
        f1.suptitle("shapefile areas", fontsize=16)
        ax1 = shapefile.plot(ax=ax1, linewidth=0.2, edgecolor='grey', )
        ax1.set_axis_off()

    # Combine shapefile with nomisr
    combined_sets = shapefile.set_index(shapefilekey).join(nomisr.set_index(nomisrKey)).reset_index()

    if barchart != 'off':
        '''Create barchart set'''
        bar_set = combined_sets[combined_sets.C_RELPUK11_NAME == subset]
        bar_set.sort_values(["OBS_VALUE"], axis=0, ascending=False, inplace=True)
        '''Map  of UK based on value nomisr'''
        sns.set_style("white")
        fig, axes = plt.subplots(1, 2, figsize=(15, 7), constrained_layout=True)
        fig.suptitle(title, fontsize=16)
        axes[0] = combined_sets[combined_sets.C_RELPUK11_NAME == subset].plot(column="OBS_VALUE",
                                                                              cmap=cmap,
                                                                              linewidth=0.2,
                                                                              edgecolor='grey',
                                                                              ax=axes[0],
                                                                              legend=True)
        axes[0].axis("off")

        '''Barchart'''

        axes[1] = sns.barplot(x="OBS_VALUE",
                              y='GEOGRAPHY_NAME',
                              data=bar_set,
                              palette=mpl.cm.ScalarMappable(cmap=cmap).to_rgba(bar_set["OBS_VALUE"]))

        axes[1].set_ylabel('')
        axes[1].set_xlabel('')
        axes[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        axes[1].spines['right'].set_visible(False)
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['bottom'].set_visible(False)

        # set individual bar lables using above list
        for i in axes[1].patches:
            # get_width pulls left or right; get_y pushes up or down
            axes[1].text(i.get_width() + .5, i.get_y() + .45,
                         str(round((i.get_width()), 2)) + '%', fontsize=12, color='black')


    else:
        '''Map  of UK based on value nomisr'''
        fig, axes = plt.subplots(1, figsize=(10, 6))
        fig.suptitle(title, fontsize=16)
        axes = combined_sets[combined_sets.C_RELPUK11_NAME == subset].plot(column="OBS_VALUE",
                                                                           cmap=cmap,
                                                                           linewidth=0.2,
                                                                           edgecolor='grey',
                                                                           ax=axes,
                                                                           legend=True)
        axes.axis("off")
    return axes
