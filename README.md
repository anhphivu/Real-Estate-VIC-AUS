# Generic Real Estate Consulting Project
## The University of Melbourne - MAST30034
This shows how to recreate our result. For more information, please read summary.ipynb

## Group member
 + `Chanh Thanh Tang`
 + `Anh Phi Vu`
 + `Ngoc Nhu Quynh Ho`
 + `Connor Liu`
 + `Duc Hoang Nguyen`

## Introduction
This project aims to complete the following 3 objective:
+ Identify key internal and external features that influence rental price
+ Identify the top 10 regions with the highest predicted growth rates
+ Determine the most liveable and affordable region



## Datasets
 + Properties Data: scraped from domain.com on 28/09/2023.
 + External Data: visit `scripts/external_datasets.py` for more information
 + Spatial data: retrieved using Google Map API on 28/09/2023



## Initial Set Up
1. Workspace
    - Clone the project to a new folder and create a new python enviroment.
    - Make sure to have file to be executed in the directory containing it.
    - Install every package in `requirements.txt` with 
        ```
        pip install -r requirements.txt
        ```
2. Create api key

    - Go to google map service and create an API that has all map service
    - Create google.env in `credential`
    - Save the key to credential as KEY1="key" in google.env, if you have more keys, save it as KEY2="key2", ...
    - If you don't want to use the api for the data, contact chanhthanht@student.unimelb.edu.au for the data




## Directories
+ credential: saved API key
+ data: saved data
+ markdown-img: images for rendering markdown in jupyternotebook
+ models: notebooks containing our models
+ notebooks: all other notebooks
+ plots: saved plots from our code
+ scripts: general python script

## Pipeline

To recreate our results, the files must be run in the following order:
<ol>
<h3>scripts/</h3>
        <li><code>domain_rent_scrape.py</li></code>
        <li><code>external_datasets.py</li></code>
<h3>notebooks/preprocess-raw</h3>
        <li><code>properties_domain_to_raw.ipynb</li></code>
        <li><code>annual_rent_to_raw.ipynb</li></code>
        <li><code>crime_to_raw.ipynb</li></code>
        <li><code>income_to_raw.ipynb</li></code>
        <li><code>population_to_raw.ipynb</li></code>
        <li><code>school_location_to_raw.ipynb</li></code>
<h3>notebooks/preprocess-curated</h3>
        <li><code>properties_domain_to_curated.ipynb</li></code>
        <li><code>annual_rent_to_curated.ipynb</li></code>
        <li><code>crime_to_curated.ipynb</li></code>
        <li><code>income_to_curated.ipynb</li></code>
        <li><code>population_to_curated.ipynb</li></code>
        <li><code>school_location_to_curated.ipynb</li></code>
<h3>notebooks/spatial-data</h3>
        <li><code>infrastructure.ipynb</code></li>
        <li><code>distance.ipynb</code></li>
        <li><code>region_to_SA2.ipynb</code></li>
<h3>notebooks/</h3>
        <li><code>merge_data.ipynb</code></li>
<h3>models/</h3>
        <li><code>full_model.ipynb</code></li>
        <li><code>sa2_model.ipynb</code></li>
</ol>