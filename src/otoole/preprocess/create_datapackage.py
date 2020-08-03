"""Creates a datapackage from a collection of CSV files of OSeMOSYS input data

- Uses Frictionless Data datapackage concept to build a JSON schema of the dataset
- Enforces relations between sets and indices in parameter files
"""

import logging
import os
import sys

from datapackage import Package
from sqlalchemy import create_engine

from otoole import read_config, read_packaged_file
from otoole.preprocess.datafile_to_datapackage import write_default_values
from otoole.preprocess.longify_data import main as longify

logger = logging.getLogger()


def generate_package(path_to_package, path_to_config = None):
    """Creates a datapackage in folder ``path_to_package``

    [{'fields': 'REGION', 'reference': {'resource': 'REGION', 'fields': 'VALUE'}}]
    """

    datapath = os.path.join(path_to_package)
    package = Package(base_path=datapath)

    package.infer("data/*.csv")

    package.descriptor["licenses"] = [
        {
            "name": "CC-BY-4.0",
            "path": "https://creativecommons.org/licenses/by/4.0/",
            "title": "Creative Commons Attribution 4.0",
        }
    ]

    package.descriptor["title"] = "The OSeMOSYS Simplicity Example Model"

    package.descriptor["name"] = "osemosys_model_simplicity"

    package.descriptor["contributors"] = [
        {
            "title": "Will Usher",
            "email": "wusher@kth.se",
            "path": "http://www.kth.se/wusher",
            "role": "author",
        }
    ]

    package.commit()

    config = read_config(path_to_config)

    new_resources = []
    for resource in package.resources:

        descriptor = resource.descriptor

        name = resource.name
        if config[name]["type"] == "param":

            indices = config[name]["indices"]
            logger.debug("Indices of %s are %s", name, indices)

            foreign_keys = []
            for index in indices:
                key = {
                    "fields": index,
                    "reference": {"resource": index, "fields": "VALUE"},
                }
                foreign_keys.append(key)

            descriptor["schema"]["foreignKeys"] = foreign_keys
            descriptor["schema"]["primaryKey"] = indices
            descriptor["schema"]["missingValues"] = [""]

        new_resources.append(descriptor)

    package.descriptor["resources"] = new_resources
    package.commit()

    filepath = os.path.join(path_to_package, "datapackage.json")
    package.save(filepath)


def validate_contents(path_to_package):

    filepath = os.path.join(path_to_package)
    package = Package(filepath)

    for resource in package.resources:
        try:
            if resource.check_relations():
                logger.info("%s is valid", resource.name)
        except KeyError as ex:
            logger.warning("Validation error in %s: %s", resource.name, str(ex))


def main(wide_folder, narrow_folder, path_to_config = None):
    longify(wide_folder, narrow_folder)
    generate_package(narrow_folder, path_to_config)
    absolute_path = os.path.join(narrow_folder, "datapackage.json")
    validate_contents(absolute_path)


def csv_to_datapackage(path_to_csv_folder: str, path_to_config: str = None) -> None:
    """Adds the datapackage.json file to a folder of CSV files

    Arguments
    ---------
    path_to_csv_folder : str
        Path to the folder of csv files
    """
    datapackage = read_packaged_file("datapackage.json", "otoole.preprocess")
    filepath = os.path.join(path_to_csv_folder, "datapackage.json")
    with open(filepath, "w") as destination:
        destination.writelines(datapackage)
    write_default_values(path_to_csv_folder, path_to_config)


def convert_datapackage_to_sqlite(path_to_datapackage, sqlite):
    """Load and save table to SQLite
    """
    dp = Package(path_to_datapackage)
    engine = create_engine("sqlite:///{}".format(sqlite))
    dp.save(storage="sql", engine=engine)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    wide_folder = sys.argv[1]
    narrow_folder = sys.argv[2]
    main(wide_folder, narrow_folder)
