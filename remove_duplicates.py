import csv
from enum import Enum
from thefuzz import fuzz

import sys, getopt

def read_map( filename: str ) -> {}:

    res = {}

    with open( filename ) as csvfile:
        reader = csv.reader( csvfile, delimiter=';' )
        for row in reader:
            [k,v] = row[0:2]
            k = int( k )
            res[ k ] = v

    print( f"INFO: read {len(res)} records from {filename}" )

    return res

def write_map( filename: str, m: {} ) -> None:

    writer = csv.writer( open( filename, "w" ), delimiter=';', lineterminator='\n' )

    for k, v in m.items():
        writer.writerow( ( v ) )

    print( f"INFO: wrote {len(m)} records to {filename}" )

def remove_all_whitespaces( w: str ) -> str:
    return ''.join(w.split())

def remove_all_nonalphanum( w: str ) -> str:
    return ''.join(e for e in w if e.isalnum())

def refine_word( w: str ) -> str:

    w1 = remove_all_nonalphanum( w )

    w2 = w1.lower()

    return w2

def refine_map( m: {} ) -> {}:

    res = {}

    for k, v in m.items():
        res[ k ] = refine_word( v )

    return res

class SimilarityType(int,Enum):
    DIFFERENT = 0
    SIMILAR   = 1
    DUPLICATE = 2

def check_similarity( w_1: str, w_2: str ) -> SimilarityType:
    r = fuzz.ratio( w_1, w_2 )

    if r >= 95:
        return SimilarityType.DUPLICATE
    elif r >= 80:
        return SimilarityType.SIMILAR

    return SimilarityType.DIFFERENT

def remove_duplicates( map_a: {}, map_b: {} ) -> [{}, {}]:

    res_a = {}
    res_b = {}

    map_a_refined = refine_map( map_a )
    map_b_refined = refine_map( map_b )

    processed_keys = {}

    for k, v in map_a_refined.items():

        processed_keys[ k ] = 1

        matches = []

        orig_v = map_a[ k ]

        # put initial word
        matches.append( orig_v )

        for k_2, v_2 in map_a.items():
            if k_2 in processed_keys:
                continue

            similarity_type = check_similarity( v, v_2 )

            if similarity_type == SimilarityType.DUPLICATE:
                # duplicate, just ignore it
                processed_keys[ k ] = 1
            elif similarity_type == SimilarityType.SIMILAR:
                # similar, but not a duplicate, add it
                processed_keys[ k ] = 1
                orig_v_2 = map_a[ k_2 ]
                matches.append( v_2 )
            else:
                # do nothing
                pass

        res_a[ k ] = matches

    return [ res_a, res_b ]

def process( inp_filenames: [str], outp_filenames: [str] ):

    num_req = 0

    map_a = read_map( inp_filenames[0] )
    map_b = read_map( inp_filenames[1] )

    res_a, res_b = remove_duplicates( map_a, map_b )

    write_map( res_a, outp_filenames[0] )
    write_map( res_b, outp_filenames[1] )

def main( argv ):

    input_files  = []
    output_files = []
    loglevel    = 0

    try:
        opts, args = getopt.getopt(argv,"hHdi:t:l:o:D",["HEADLESS","dry","DEBUG","ifile=","type=","limit=","offset="])
    except getopt.GetoptError:
        print( 'remove_duplicates.py [-H]' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'remove_duplicates.py [-H]' )
            sys.exit( 0 )
        elif opt in ("-D", "--DEBUG"):
            loglevel = 1
        elif opt in ("-i", "--ifile"):
            input_files = arg.split(',')
        elif opt in ("-o", "--ofile"):
            output_files = arg.split(',')

    #set_loglevel( loglevel )

    print( f"DEBUG: num input file = {len(input_files)}" )

    if len( input_files ) != 2:
        print( "FATAL: need 2 comma-separated input filenames" )
        sys.exit( 1 )

    if len( output_files ) != 2:
        print( "FATAL: need 2 comma-separated output filenames" )
        sys.exit( 1 )

    process( input_files, output_files )

    sys.exit( 0 )

if __name__ == '__main__':
    main( sys.argv[1:] )
