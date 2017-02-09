import click
import json

@click.command()
@click.argument('infile', type=click.File(), required=True)
@click.argument('outfile', type=click.File('w'), required=True)

def json2geojson(infile, outfile):
    """
    Convert a JSON file to GeoJSON

    Parameters
    ------------------------------
    INFILE.json
    OUTFILE.geojson

    Returns
    ------------------------------
    OUTFILE.geojson
    """

    # SPECIFY INFILE
    src = json.load(infile)

    if str(src) == '[]':
        print('ERROR, INFILE: ', infile, ' IS BLANK: ', src)
        return
    # EXTRACT THE CLUSTER ID AND THE YEAR FROM THE FILE NAME
    cluster_id = str(infile).split('_')[1]
    year = str(infile).split('_')[2]

    # EXTRACT THE DELINEATION TYPE (WET OR DRY)
    pad_type = str(infile).split('_')[-1].split('.')[0]

    # EXTRACT METADATA FROM THE INFILE
    map_site = src[0][u'meta'][u'mapSite']
    cluster_distance = src[0][u'meta'][u'clusterDistance']
    table_id = src[0][u'meta'][u'tableId']
    date = src[0][u'meta'][u'date']
    diameter = src[0][u'diameter']
    nearest = src[0][u'nearest']

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
            outer_coords = [[coord["lng"], coord["lat"]] for coord in item[u'polygon'][u'outer']]
            end_point = outer_coords[0]
            outer_coords.append(end_point)
            outer_pts.append(outer_coords)

    if inner_polygon is not 'null':
        for item in src:
            inner_coords = [[coord["lng"], coord["lat"]] for coord in item[u'polygon'][u'inner']]
            end_point = inner_coords[0]
            inner_coords.append(end_point)
            inner_pts.append(inner_coords)

    if test_polygon is not 'null':
        for item in src:
            test_coords = [[coord["lng"], coord["lat"]] for coord in item[u'polygon'][u'test']]
            end_point = test_coords[0]
            test_coords.append(end_point)
            test_pts.append(test_coords)

    # # HANDLE ISSUES ARISING FROM REPETITION OF POLYGONS
    if str(outer_pts) == '[]':
        outer_pts.append(filter(None, outer_pts))
    if str(outer_pts) != '[]':
        pass

    if str(inner_pts) == '[]':
        inner_pts.append(filter(None, inner_pts))
    if str(inner_pts) != '[]':
        pass

    if str(test_pts) == '[]':
        test_pts.append(filter(None, test_pts))
    if str(test_pts) != '[]':
        pass

    outer_pts_2 = outer_pts[0]
    inner_pts_2 = inner_pts[0]
    test_pts_2 = test_pts[0]

    # prime_ID = src[0][u'markers'][0][u'row']

    # SPECIFY THE OUTPUT DATA FORMAT
    dst = {"type": "FeatureCollection",
           "features": [{"type": "Feature",
                         "properties": {
                             # "polyId":"Outer",
                             "tableId":table_id,
                             "mapSite":map_site,
                             "clusterDistance":cluster_distance,
                             "date":date,
                             "cluster_id":cluster_id,
                             "delineation_type":pad_type,
                             "classification_year":year,
                             "diameter":diameter,
                             "nearest":nearest},
                         "geometry": {"type": "MultiPolygon",
                                      "coordinates":[[inner_pts_2], [outer_pts_2], [test_pts_2]]}}
                        ]
           }
    output = json.dumps(dst)
    outfile.write(output)

if __name__ == '__main__':
    json2geojson()
