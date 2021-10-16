""" Script example for vizualisation models """
import pandas as pd
from urllib.parse import urljoin
from src.mainprog import loadShapefiles, plot_nomisr_shapefile
import src.confiq

# load the Zip shape files ---------------------------------------------------------------------------------------------
map_df = loadShapefiles(urljoin(src.confiq.PUBLIC_REPO, src.confiq.SHAPEFILE_DISTRICTS))

# Example for religion data,  ------------------------------------------------------------------------------------------
df = pd.read_csv(urljoin(src.confiq.PUBLIC_REPO, 'nomis_religion.csv'))

# Plot in whole UK map census data for religion
plot_nomisr_shapefile(nomisr=df,
                      shapefile=map_df,
                      shapefilekey='lad18cd',
                      subset="Christian",
                      cmap="winter",
                      title="Population reporting Christian, 2011, England and Wales local and unitary authorities (%)")

# Sub select specific counties, ie. for Northamptonshire and its neighbours area
counties = ['Northamptonshire',
            'Central Bedfordshire',
            'Milton Keynes',
            'Bedford',
            'Leicestershire',
            'Leicester',
            'Rutland',
            'Peterborough',
            'Cambridgeshire',
            'Oxfordshire',
            'Buckinghamshire',
            'Warwickshire']

plot_nomisr_shapefile(nomisr=df[df['GEOGRAPHY_CODE'].isin(map_df['lad18cd'][map_df['county'].isin(counties)])],
                      shapefile=map_df,
                      shapefilekey='lad18cd',
                      subset="Christian",
                      cmap="winter",
                      title="Population reporting Christian, 2011, Northamptonshire and neighbours (%)",
                      barchart="On")
