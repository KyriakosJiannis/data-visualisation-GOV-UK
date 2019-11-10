"""script which contain examples vizualisation examples from """
import pandas as pd
from mainprog import loadShapefiles, plot_nomisr_shapefile

# load the shape files from Pcloud, files extracted from
shapefilezip1 = 'https://filedn.com/lK8J7mCaIwsQFcheqaDLG5z/data/ukdata/united-kingdom-local-authority-districts' \
                '-december-2018.zip'
shapefilezip2 = 'https://filedn.com/lK8J7mCaIwsQFcheqaDLG5z/data/ukdata/united-kingdom-counties-and-unitary' \
                '-authorities-december-2017.zip'

map_df1 = loadShapefiles(shapefilezip1)
map_df2 = loadShapefiles(shapefilezip2)

"""Religion example"""
# load the files from Pcloud, files extracted using R Api nomis
df1 = pd.read_csv('https://filedn.com/lK8J7mCaIwsQFcheqaDLG5z/data/ukdata/nomis.religion.csv')
df2 = pd.read_csv('https://filedn.com/lK8J7mCaIwsQFcheqaDLG5z/data/ukdata/nomis.religion2.csv')


# plot all available
plot_nomisr_shapefile(nomisr=df1,
                      shapefile=map_df1,
                      shapefilekey='lad18cd',
                      subset="Christian",
                      cmap="winter",
                      title="Population reporting Christian, 2011, England and Wales local and unitary authorities (%)")

# sub selection specific counties, ie. for Northamptonshire and its neighbours area
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

plot_nomisr_shapefile(nomisr=df1[df1['GEOGRAPHY_CODE'].isin(map_df1['lad18cd'][map_df1['county'].isin(counties)])],
                      shapefile=map_df1,
                      shapefilekey='lad18cd',
                      subset="Christian",
                      cmap="winter",
                      title="Population reporting Christian, 2011, Northamptonshire and neighbours (%)",
                      barchart="On")