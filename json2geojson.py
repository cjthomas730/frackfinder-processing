import click
import json

@click.command()
@click.argument('infile', type=click.File(), required=True)
@click.argument('outfile', type=click.File('w'), required=True)

def json2geojson(infile, outfile):
    """
    Convert a JSON file to GeoJSON
    Parameters
    ----------
    infile.json
    outfile.geojson

    Returns
    -------
    """
    # SPECIFY INFILE
    src = json.load(infile)

    # SPECIFY POSSIBLE POLYGON GEOMETRIES
    polygon_geometries = src[0][u'polygon']
    outer_polygon = json.dumps(polygon_geometries[u'outer'])
    inner_polygon = json.dumps(polygon_geometries[u'inner'])
    test_polygon = json.dumps(polygon_geometries[u'test'])

    outer_pts = []
    inner_pts = []
    test_pts = []

    if outer_polygon is not None:
        for item in src:
            outer_coords = [[coord["lat"], [coord["lng"]]] for coord in item[u'polygon'][u'outer']]
            outer_pts.append(outer_coords)

    if inner_polygon is not 'null':
        for item in src:
            inner_coords = [[coord["lat"], [coord["lng"]]] for coord in item[u'polygon'][u'inner']]
            inner_pts.append(inner_coords)

    if test_polygon is not 'null':
        for item in src:
            test_coords = [[coord["lat"], [coord["lng"]]] for coord in item[u'polygon'][u'test']]
            test_pts.append(test_coords)


    # EXTRACT METADATA FROM THE INFILE
    mapSite = src[0][u'meta'][u'mapSite']
    clusterDistance = src[0][u'meta'][u'clusterDistance']
    tableId = src[0][u'meta'][u'tableId']
    date = src[0][u'meta'][u'date']
    diameter = src[0][u'diameter']
    nearest = src[0][u'nearest']

    # SPECIFY THE OUTPUT DATA FORMAT
    dst = {"type": "FeatureCollection",
                      "features": [{"type": "Feature",
                                    "properties": {
                                        "tableId":tableId,
                                        "mapSite":mapSite,
                                        "clusterDistance":clusterDistance,
                                        "date":date,
                                        "diameter":diameter,
                                        "nearest":nearest},
                                    "geometry": {"type": "Polygon",
                                                 "coordinates":outer_pts}},
                                   {"type": "Feature",
                                    "properties": {
                                        "tableId":tableId,
                                        "mapSite":mapSite,
                                        "clusterDistance":clusterDistance,
                                        "date":date,
                                        "diameter":diameter,
                                        "nearest":nearest},
                                    "geometry": {"type": "Polygon",
                                                 "coordinates":inner_pts}},
                                   {"type": "Feature",
                                    "properties": {
                                        "tableId":tableId,
                                        "mapSite":mapSite,
                                        "clusterDistance":clusterDistance,
                                        "date":date,
                                        "diameter":diameter,
                                        "nearest":nearest},
                                    "geometry": {"type": "Polygon",
                                                 "coordinates":test_pts}},
                                   ]
           }
    output = json.dumps(dst)

    outfile.write(output)

if __name__ == '__main__':
    json2geojson()
