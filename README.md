# data-visualisation-GOV-UK

Visualise UK map at district / unitary level or coutry level, using UK <b>shapefile</b> from https://public.opendatasoft.com and UK measurements from <b> nomisr  R API </b> https://cran.r-project.org/web/packages/nomisr/vignettes/introduction.html and plot maps with or without bar plot. 

* For visualisation uses <b> matplotlib, seaborn </b>
* For shapefiles <b> geopandas </b>

<b> plot_nomisr_shapefile </b> :
<br> combines nomisr data, with UK shapefiles and plot statistics on map


#### Examples for religion census UK:

```python
plot_nomisr_shapefile(nomisr=df, #nomisr data with measurements
                      shapefile=map_df, #shapefile
                      shapefilekey='lad18cd', #shapefile key column
                      subset="Christian",  #file subset
                      cmap="winter",  #cmap colours
                      title="Population reporting Christian, 2011, England and Wales local and unitary authorities (%)")
```

#### Output:
 ![Screenshot](./output/Figure_1.png)

```python
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

plot_nomisr_shapefile(nomisr=df[df['GEOGRAPHY_CODE'].isin(map_df['lad18cd'][map_df['county'].isin(counties)])],
                      shapefile=map_df,
                      shapefilekey='lad18cd',
                      subset="Christian",
                      cmap="winter",
                      title="Population reporting Christian, 2011, Northamptonshire and neighbours (%)",
                      barchart="On")
```
#### Output:
 ![Screenshot](./output/Figure_2.png)
