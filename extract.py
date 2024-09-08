"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach # Import the build classes to create instances of neos and cads


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Header names of the fields needed to create a NearEarthObject, in the order as
    # given in the NearEarthObject __init__ (designation, name, diameter, hazardous), 
    # to extract the necessary data from the neo csv.
    header_names = ["pdes", "name", "diameter", "pha"]
 
    # Load the neo csv file and read the header separately.
    data = []
    with open(neo_csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        # Define the corresponding index for getting the correct field in each row 
        # for each header_name
        indexes = [header.index(header_name) for header_name in header_names]
        for row in reader:
            # Create a NearEarthObject from the data in the current row, using the 
            # the correct index each defined field in header_names.
            data.append(NearEarthObject(*[row[index] for index in indexes]))

    return data



def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, "r") as f:
        reader = json.load(f)
        # key-value mapping for corresponding json keys "fields" and "data" via indexing 
        reader = [dict(zip(reader["fields"], data)) for data in reader["data"]] 

        approaches = [] #Create an empty list to store CloseApproach Object instances

        # create instance object of cad for observations with complete data
        for line in reader:
            if "des" in line and "cd" in line and "dist" in line and "v_rel" in line:
                approach = CloseApproach(
                    designation=line["des"],
                    time=line["cd"],
                    distance=float(line["dist"]),
                    velocity=float(line["v_rel"]),
                )
                approaches.append(approach)
            else:
                print("Missing criticial information in observation in line:", line)
    return approaches
