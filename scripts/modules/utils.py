import os
import json
import zipfile
import requests
import uuid
from IPython.display import display_javascript, display_html, display

class RenderJSON(object):
    """This makes the output of jupyterbook into a expandable and collapable json
    src: 
    https://www.reddit.com/r/IPython/comments/34t4m7/lpt_print_json_in_collapsible_format_in_ipython/
    
    Args:
        object (dict|jsontext): json data
    """    ''''''
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, str):
            self.json_str = json.loads(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], 
                    function() {
                        renderjson.set_icons('+', '-')
                                        .set_show_to_level(1);
                        document.getElementById('%s').appendChild(renderjson(%s));
        });
        """ % (self.uuid, self.json_str), raw=True)


def download_file(url, path):
    """This function download file from the given url and save it in the desinated path

    Args:
        url (str): the url to download from
        path (str): path to where to save the downloaded file
    """    
    filename = path.split('/')[-1]
    try:
        req = requests.get(url)
        with open(path, 'wb') as file:
            file.write(req.content)
        print(f"Downloaded {filename}")
    except Exception as error:
        print(f'\nError with file {filename}')
        print(f'    {error}\n')

def unzip_file(zip_file_path, dest_folder):
    """This function unzip file into selected folder

    Args:
        zip_filepath (str): path to zip file
        dest_folder (str): destination of unzipped file
    """    
    filename = zip_file_path.split('/')[-1]
    try: 
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)
        print(f'    Unzipped {filename} successfully')
    except Exception as error:
        print(f'\n    Failed to unzip {filename}')
        print(f'        {error}\n')
    

