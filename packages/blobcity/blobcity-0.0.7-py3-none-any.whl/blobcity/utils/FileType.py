# Copyright 2021 BlobCity, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This Python File consists of function to fetch and read dataset from various datasource using pandas framework.
"""


import os.path
import pandas as pd
import io
import requests
from requests.models import HTTPError
def get_dataframe_type(file_path,dc=None):

    """
    param1: String - System path or URL for data
    param2: Object - dictionary Class
    return: object - pandas DataFrame

    Working:
        first the function split the complete string path and fetchs the extension format of the file
        next on the basis of extension type it utilize appropriate pandas read function to get the dataframe.
        and finally return the dataframe object.
    """
    extension = os.path.splitext(file_path)[1]
    try:
        if(extension==".csv"):
            Types = "csv"
            df=pd.read_csv(file_path)
        elif extension==".xlsx":
            Types = "xlsx"
            df=pd.read_excel(file_path)
        elif extension==".parquet":
            df=pd.read_parquet(file_path)
        elif extension==".json":
            Types = "JSON"
            df=pd.read_json(file_path)
        elif extension==".pkl":
            df=pd.read_pickle(file_path)
            Types="Pickle"
    
    except HTTPError:
        response = requests.get(file_path)
        file_object = io.StringIO(response.content.decode('utf-8'))
        if(extension==".csv"):
            Types = "csv"
            df=pd.read_csv(file_object)
        elif extension==".xlsx":
            Types = "xlsx"
            df=pd.read_xlsx(file_object)
        elif extension==".excel":
            df=pd.read_excel(file_object)
        elif extension==".parquet":
            df=pd.read_parquet(file_object)
        elif extension==".json":
            Types = "JSON"
            df=pd.read_json(file_object)
        elif extension==".pkl":
            df=pd.read_pickle(file_object)
            Types="Pickle"

    if dc!=None: dc.addKeyValue('data_read',{"type":Types,"file":file_path,"class":"df"})
    return df


def write_dataframe(dataframe=None,path=""):
    """
    param1: pd.DataFrame
    param2: String
    param3: String

    Function perform validation on provided arguments for file creation.
    """
    try:
        path_components = path.split('.')
        extension = path_components[1] if len(path_components)<=2 else path_components[-1]
        if path!="":
            if isinstance(dataframe,pd.DataFrame):
                if extension in ['csv','xlsx','json']:
                    save_dataframe(dataframe,path,extension)
                else:raise TypeError("File type should be in following format [csv,xlsx,json],provided type {}".format(extension))
            else: raise TypeError("Dataframe argument must be pd.DataFrame type, provided {}".format(type(dataframe)))
        else: raise ValueError("Argument dataframe or type can't be None or empty") 
    except Exception as e:
        print(e)

def save_dataframe(dataframe,path,ftype):
    """
    param1: pd.DataFrame
    param2: String
    param3: String

    Function write pandas DataFrame at specified location with specified file type. 
    """
    try:
        if ftype=='csv':
            dataframe.to_csv(path)
        elif ftype=='xlsx':
            dataframe.to_excel(path)
        elif ftype=='json':
            dataframe.to_json(path,orient="index")
        print("saved at path {}".format(path))
    except Exception as e:
        print(e)
