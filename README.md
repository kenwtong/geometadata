# Geometadata

Geometadata adds or updates the Summary, Description and Credits metadata elements of a spatial file.
The update metadata values are read from a JSON file. Updating only the Summary, Description, and Credits metadata
elements ensures the metadata is seen immediate in ArcCatalog and keeps metadata management to a minimum.

## Dependencies
Python 2.7

## Usage
### Command Line
Run the geometadata.py script form the command prompt with the following parameters:
- -f or --file specifying the full path to your spatial file
- -m or --metadata specifying the full path to your metadata JSON file

`python geometadata.py -f <full path to spatial file> -m <full path to metadata JSON file>`

Run python `geometadata.py -h` for help with the parameters.

#### Module
You can import the geometadata module and call the the following functions:

`update_metadata(<full path to spatial file>, <full path to metadata JSON file>)`

Provide a spatial file and a JSON file with the metadata values for
Summary, Description and Credits tags. If the metadata xml file is
missing, one will be created. This is the same as running the script from the command line.

`make_metadata_file(<full path to spatial file>)`

Provide a spatial file and a basic metadata xml will be created. The
metadata xml file created will not have the Summary, Description or
Credits tags added.

### Metadata JSON file
The metadata file used for the update must be in the following format:

    {
         "dataIdInfo": {
            "idPurp": "Your summary",
            "idAbs": "You abstract",
            "idCredit": "You credit"
        }
    }


The keys in the JSON file corresponds to following sections when viewing metadata in ArcCatalog:

- idPurp = Summary
- idAbs = Abstract
- idCredit = Credits

## Limitations
Only the following types of files are currently supported:

- .jpg or .jpeg
- .png
- .shp
- .tif or .tiff

## Tips
You can run `arcpy.SynchronizeMetadata_conversion(<spatial_file>)` after to get ArcGIS to add and update metadata it automatically generates like spatial reference, extents, and attribute fields.

