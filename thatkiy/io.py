import csv
import time
import argparse
from pathlib import Path

from .distance import distance
from .geoindex import GeoIndex


def load_csv(fn):
    ext = fn.suffix
    delim = ',' if ext == '.csv' else '\t'
    with open(fn) as fh:
        reader = csv.reader(fh, delimiter=delim)
        header = next(reader)
        data = [row for row in reader]
        return header, data

def save_csv(fn, header, data, delimiter):
    with open(fn, 'w', newline='') as fh:
        writer = csv.writer(fh, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(data)


def cli():
    
    parser = argparse.ArgumentParser(description='thatkiy: calculate geodesic distances between points and sets')
    parser.add_argument('filename')
    parser.add_argument('--output','-o', action='store', help='output filename', required=True)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--timeit", help="report time", action="store_true")
    parser.add_argument('--distance','-d', action='append', help='compute distance')
    parser.add_argument('--neighbor','--neighbour','-n', action='append', help='compute neighbor and distance')
    args = parser.parse_args()

    verbose = args.verbose
    timeit = args.timeit
    if timeit: start_time = time.time()
    if verbose: print(' - Validating input...')

    # Check that the input file exists
    in_fn = Path(args.filename)
    assert in_fn.exists()

    # Check that the output file has the correct extension
    out_fn = Path(args.output)
    out_ext = out_fn.suffix
    assert out_ext in ('.raw', '.tsv', '.csv')
    out_delim = ',' if out_ext == '.csv' else '\t'

    # Load data from input file
    header, data = load_csv(in_fn)
    if verbose:
        print(' - Input file:', str(in_fn))
        print(' - Input headers:', header)

    for _ in args.distance:
        dist_name, lat, lon = validate_cli_distance(_)
        if verbose:
            print(f' - Computing distance to lat={lat} lon={lon} and storing it in "{dist_name}"')
            add_distance_to_point(header, data, lat, lon, dist_name, verbose=verbose)

    for _ in args.neighbor:
        id_name, dist_name, fn = validate_cli_neighbor(_)
        if verbose:
            print(f' - Computing distance to nearest neighbor within {fn}; storing distance in "{dist_name}" and neighbor id in "{id_name}"')
            add_distance_to_point(header, data, lat, lon, dist_name, verbose=verbose)
            add_neighbor(header, data, fn, id_name, dist_name, verbose=verbose)

    if verbose: print(f' - Saving output in {out_fn}')
    save_csv(out_fn, header, data, delimiter=out_delim)
    if verbose: print('\nDone!')
    if timeit: print("--- {:7.3f} seconds ---".format(time.time() - start_time))


def add_distance_to_point(header, data, lat, lon, name, verbose=False):
    assert name not in header
    header.append(name)

    lat_i = header.index('lat')
    lon_i = header.index('lon')

    for i, row in enumerate(data, 1):
        if verbose and (i % 1000 == 0):
            print('.', end='', flush=True)
        row_lat, row_lon = float(row[lat_i]), float(row[lon_i])
        dist = distance(row_lat, row_lon, lat, lon)
        row.append(f'{dist:.4f}')
    if verbose and i >= 1000:
        print()


def get_coords(header, data):
    lat_i = header.index('lat')
    lon_i = header.index('lon')
    id_i = header.index('id')
    #print(header)
    #print(id_i, lat_i, lon_i)
    coords = [(int(row[id_i]), float(row[lat_i]), float(row[lon_i])) for row in data]
    return coords


def add_neighbor(header, data, fn, name_neighbor, name_distance, verbose=False):
    
    # Create index
    neigh_header, neigh_data = load_csv(fn)
    if verbose:
        print(' - neighbor headers:', neigh_header)
    coords = get_coords(neigh_header, neigh_data)
    idx = GeoIndex(data=coords)

    assert name_neighbor not in header
    assert name_distance not in header
    header.extend([name_neighbor, name_distance])
    lat_i = header.index('lat')
    lon_i = header.index('lon')
    id_i = header.index('id')

    for i, row in enumerate(data, 1):
        if verbose and (i % 1000 == 0):
            print('.', end='', flush=True)
        lat = float(row[lat_i])
        lon = float(row[lon_i])
        identifier = int(row[id_i])

        nn = idx.nearest(lat, lon, identifier=identifier)
        dist = distance(lat, lon, *idx.coords[nn])
        row.extend([nn, f'{dist:.4f}'])
    if verbose and i >= 1000:
        print()


def validate_cli_distance(input):
    input = input.split(',')
    assert len(input) == 3, f'--distance requires a (name,lat,lon) list,  but received {input}'
    name, lat, lon = input
    lat = float(lat)
    lon = float(lon)
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180
    return name, lat, lon


def validate_cli_neighbor(input):
    input = input.split(',')
    assert len(input) == 3, f'--neighbor requires a (name_id, name_dist, fn) list,  but received {input}'
    id_name, dist_name, fn = input
    fn = Path(fn)
    assert fn.exists()
    return id_name, dist_name, fn


