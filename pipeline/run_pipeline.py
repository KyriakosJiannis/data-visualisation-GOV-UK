import os
import sys
from urllib.parse import urljoin
import configparser
import logging
import warnings

warnings.filterwarnings("ignore")

# Get the absolute path of the current script, and project's root directory dynamically
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))
sys.path.append(project_root)

from src.analysis.analysis_module import load_data_and_merge, subset_religion_gdf, plot_nomis_data


# Configure the logging module
logging.basicConfig(filename='run_pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def run_pipeline(config_file_path):
    """
    Run the data visualization pipeline.


    Parameters:
    - config_file_path (str): The path to the configuration file.
    """

    if not os.path.exists(config_file_path):
        logging.error(f'Config file not found: {config_file_path}')
        sys.exit(1)  # Exit the script with an error cod

    # Load configuration
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Access configuration values
    input_dir = config['directories']['input_dir']
    output_dir = config['directories']['output_dir']
    public_repo = config['directories']['public_repo']
    opendata_shapefile_districts = config['shapefiles']['districts']
    nomis_csv_url = urljoin(public_repo, 'nomis_religion.csv')

    # Construct full paths
    input_dir_path = os.path.join(project_root, input_dir)
    output_dir_path = os.path.join(project_root, output_dir)
    opendata_shapefile_districts_url = urljoin(public_repo, opendata_shapefile_districts)

    # Load date and merge
    try:
        merged_gdf = load_data_and_merge(nomis_csv_url, opendata_shapefile_districts_url, nomis_key="GEOGRAPHY_CODE", geo_key='lad18cd')
        logging.info('Data loaded and merged successfully.')

    except Exception as e:
        logging.error(f'Error loading data merged: {e}')

    # Sub-Select
    subset_df = subset_religion_gdf(merged_gdf, 'Christian')

    # Plot in the whole UK map
    try:
        plot_nomis_data(
            geo_data=subset_df,
            cmap="winter",
            title="Population reporting Christian 2011, \n England and Wales local and unitary authorities (%)",
            save_path=os.path.join(output_dir_path, 'religions_plot_bar1.png')
        )
        logging.info('First plot created successfully.')
    except Exception as e:
        logging.error(f'Error creating first plot: {e}')

    # Sub-select specific counties
    counties = ['Northamptonshire', 'Central Bedfordshire', 'Milton Keynes', 'Bedford', 'Leicestershire', 'Leicester',
                'Rutland', 'Peterborough', 'Cambridgeshire', 'Oxfordshire', 'Buckinghamshire', 'Warwickshire']

    # Plot in specific counties
    try:
        plot_nomis_data(
            geo_data=subset_df[subset_df['county'].isin(counties)],
            cmap="winter",
            title="Population reporting Christian 2011, \n Northamptonshire and neighbours (%)",
            barchart="On",
            save_path=os.path.join(output_dir_path, 'religions_plot_bar2.png')
        )
        logging.info('Second plot created successfully.')
    except Exception as e:
        logging.error(f'Error creating second plot: {e}')


if __name__ == "__main__":
    os.chdir(project_root)
    config_file_path = 'config/config.ini'
    run_pipeline(config_file_path)
    logging.info('Pipeline execution completed successfully.')
