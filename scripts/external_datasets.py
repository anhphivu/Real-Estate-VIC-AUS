'''This script download external dataset and unzip them if needed to data/landing
'''
from modules.utils import download_file, unzip_file

LANDING = 'data/landing/'

if __name__ == "__main__":
    # 2001 - 2022 population by SA2 region spreadsheet
    download_file('https://www.abs.gov.au/statistics/people/population/regional-population/2021-22/32180DS0003_2001-22r.xlsx',
                            LANDING + 'SA2_Population.xlsx')

    # income by SA2 region spreadsheet
    download_file('https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2015-16-2019-20/6524055002_DO001.xlsx', 
                            LANDING + 'SA2_Income.xlsx')
    # boundaries of SA2 regions shapefile
    download_file('https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip',
                           LANDING + 'SA2_Borders.zip')
    unzip_file(LANDING + 'SA2_Borders.zip', LANDING)

    # school locations
    download_file('https://www.education.vic.gov.au/Documents/about/research/datavic/dv346-schoollocations2023.csv', 
                            LANDING + 'School_Locations.csv')

    # past rental price by suburb
    download_file('https://www.dffh.vic.gov.au/moving-annual-rents-suburb-march-quarter-2023-excel', 
                            LANDING + 'moving_annual_rent.xlsx')
    
    # Crime data
    download_file('https://files.crimestatistics.vic.gov.au/2023-06/Data_Tables_LGA_Recorded_Offences_Year_Ending_March_2023.xlsx',
                            LANDING + 'crime_stat_March_2023.xlsx')

    # train station location shapefile
    # download_file('https://s3.ap-southeast-2.amazonaws.com/cl-isd-prd-datashare-s3-delivery/Order_QHA71K.zip?orderid=I06SYD', 
    #                         LANDING + 'train_stations.zip')
    # unzip_file(LANDING + 'train_stations.zip', LANDING)

    # postcode csv
    # download_file('https://www.matthewproctor.com/Content/postcodes/australian_postcodes.csv', 
    #                         LANDING + 'postcode_surbubs.csv')

    # population projection data
    # **OLD** SA2 regions
    # download_file('https://www.planning.vic.gov.au/__data/assets/excel_doc/0035/628694/VIF2019-population-in-5-years-2036-asgs.xlsx', 
    #                         LANDING + 'SA2_Projection.xlsx')
    
    # ABS medium series projection with no SA2 regions
    # download_file('https://www.abs.gov.au/statistics/people/population/population-projections-australia/2017-base-2066/32220_table_b2.xls',
    #                         LANDING + 'Vic_Projection.xls')
    
    
    