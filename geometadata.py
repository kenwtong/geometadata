#-------------------------------------------------------------------------------
# Name:        geometadata.py
# Version:     0.15
#
# Purpose:     Update the metadata in an XML file of a Shapefile, GeoTiff,
#              JPG or PNG.
#
#              If the XML metadata file does not exist one will be created.
#              ArcCatalog will fill in the rest of the information when you view
#              the metadata in the Description tab.
#
# Author:      Ken Tong
#
# Created:     17/06/2015
# Updated:     19/06/2015
#-------------------------------------------------------------------------------

import argparse
import collections
import ConfigParser
import json
import os
import shutil
import sys
import xml.etree.cElementTree as et


def __get_spatial_file_xml(spatial_file):
    """
        Check to see if the provided spatial file exists. If it
        it does, the function will return the metada XML file for the spatial
        file. If the XML file does not exist, one will be created.

        Parameters:
        @spatial_file: Full path to the Shapefile that will have its metadata updated.

        Returns:
        @spatial_file_xml: Full path to the XML file of the input spatial file.

        A skeleton metadata XML file will also be created if necessary.
    """
    SPATIAL_EXTENSIONS_LIST = ['.jpg', '.jpeg', '.png', '.shp', '.tif', '.tiff']

    if os.path.isfile(spatial_file):
        filename = os.path.splitext(os.path.basename(spatial_file))[0]
        extension = os.path.splitext(os.path.basename(spatial_file))[1]
        if extension in SPATIAL_EXTENSIONS_LIST:
            print 'Spatial file found:', spatial_file
            spatial_file_xml = '.'.join([spatial_file, 'xml'])
            if not os.path.isfile(spatial_file_xml):
                print 'No metadata XML file found. Creating {0}'.format(spatial_file_xml)
                make_metadata_file(spatial_file)
                print 'Metadata XML file created.'
            return spatial_file_xml
        else:
            print '{0} doesn\'t seem to be a supported file format.'.format(spatial_file)
            sys.exit()
    else:
        print 'Cannot find file:', spatial_file, '\nPlease double check the path entered.'
        sys.exit()


def make_metadata_file(spatial_file):
    """
        Create the basic structure of a metadata XML file.

        Parameters:
        @spatial_file: Full path to the XML file of the input spatial file
                           that will be created.

        Returns:
        None
    """

    def get_format_name(extension):
        """
        Function returns the long name of the spatial format.

        Parameters:
        @extension: the extension of the spatial file.

        Returns:
        @format: the name of the spatial format
        """
        format = {
            '.shp': 'Shapefile',
            '.tif': 'Raster Dataset',
            '.tiff': 'Raster Dataset',
            '.jpg': 'Raster Dataset',
            '.png': 'Raster Dataset'
        }

        return format.get(extension, 'Unknown')

    metadata = et.Element('metadata')
    dataIdInfo = et.SubElement(metadata, 'dataIdInfo')
    et.SubElement(dataIdInfo, 'idPurp')
    et.SubElement(dataIdInfo, 'idAbs')
    et.SubElement(dataIdInfo, 'idCredit')
    idCitation = et.SubElement(dataIdInfo, 'idCitation')
    resTitle = et.SubElement(idCitation, 'resTitle')
    resTitle.text = os.path.splitext(os.path.basename(spatial_file))[0]
    resTitle.set('Sync', 'TRUE')
    distInfo = et.SubElement(metadata, 'distInfo')
    distFormat = et.SubElement(distInfo, 'distFormat')
    formatName = et.SubElement(distFormat, 'formatName')
    formatName.text = get_format_name(os.path.splitext(os.path.basename(spatial_file))[1])
    formatName.set('Sync', 'TRUE')
    tree = et.ElementTree(metadata)
    tree.write('.'.join([spatial_file, 'xml']))

    return None


def __check_metadata_file(metadata_update_file):
    """
        ** Function meant for internal use **

        Check to see if the metadata JSON file exists.

        Input:
        @metadata_update_file: Full path to the Shapefile that will have its metadata updated.

        Returns:
        None
    """
    if os.path.isfile(metadata_update_file):
        return None
    else:
         print 'Cannot find file:', metadata_update_file, '\nPlease double check the path entered.'
         sys.exit()


def __update_metadata_xml(spatial_file_xml, metadata_update_file):
    """
        Update the metadata XML of a Shapefile or GeoTiff.
        A copy of the original metadat XML is created.

        Parameters:
        @spatial_file_xml: Full path to the XML file of the input spatial file
                           that will have its metadata updated.
        @metadata_update: Full path to the metadata Json file with the updated metadata.

        Returns:
        None

        Output:
        Updated metadata XML file.
    """
    with open(metadata_update_file, 'r') as metadata_json:
        metadata_dict = json.loads(metadata_json.read())
    main_element = [key for key in metadata_dict][0]
    element_list = [key for key in metadata_dict[main_element]]

    tree = et.ElementTree(file = spatial_file_xml)
    root = tree.getroot()

    if main_element not in [child.tag for child in root]:
        print 'Element {0} not in existing metadata file. Adding {0} element.'.format(main_element)
        dataIdInfo = et.SubElement(root, main_element)
    else:
        print 'Metadata element {0} already exists.'.format(main_element)
        dataIdInfo = tree.find(main_element)
    print 'Updating metadata for {0}'.format(spatial_file_xml)

    for element in element_list:
        if element not in [subchild.tag for subchild in dataIdInfo]:
            et.SubElement(dataIdInfo, element).text = metadata_dict[main_element][element]
        else:
            sub_element = tree.find(main_element).find(element)
            sub_element.text =  metadata_dict[main_element][element]

    print 'Creating backup of original metadata file.'
    shutil.copyfile(spatial_file_xml, '.'.join([spatial_file_xml, 'bak']))
    tree.write(spatial_file_xml)
    print '{0} updated successfully.\n'.format(spatial_file_xml)

    return None


def update_metadata(spatial_file, metadata_update_file):
    """
        This function updates the metadata XML of a Shapefile or GeoTiff.
        A copy of the original metadat XML is created.

        Parameters:
        @spatial_file: Full path to the Shapefile that will have its metadata updated.
        @metadata_update: Full path to the metadata Json file with the updated metadata.

        Returns:
        None
    """
    __check_metadata_file(metadata_update_file)
    metadata_xml = __get_spatial_file_xml(spatial_file)
    __update_metadata_xml(metadata_xml, metadata_update_file)
    return None


def main():
    parser = argparse.ArgumentParser(description='Update Metadata')
    parser.add_argument('-f', '--file', action='store', dest='spatial_file',
        required=True,
        help=('Full path to the Shapefile that will have its metadata updated.'
              ' File should be a Shapefile, GeoTiff, JPEG, or PNG'))
    parser.add_argument('-m', '--metadata', action='store', dest='metadata_json_file',
                        required=True, help='Full path to the metadata JSON file with the updated metadata.')
    args = parser.parse_args()
    update_metadata(args.spatial_file, args.metadata_json_file)


if __name__ == '__main__':
    sys.exit(main())