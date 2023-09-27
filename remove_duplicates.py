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

def remove_all_whitespaces( w: str ) -> str:
    return ''.join(w.split())

def clean_word( w: str ) -> str:
    return w

class SimilarityType(int,Enum):
    DIFFERENT = 0
    SIMILAR = 1
    DUPLICATE=2

def check_similarity( w_1: str, w_2: str ) -> SimilarityType:
    return 0

def remove_duplicates( map_a: {}, map_b: {} ) -> [{}, {}]:

    res_a = {}
    res_b = {}

    processed_keys = {}

    for k, v in map_a.items():

        processed_keys[ k ] = 1

        matches = []

        # put initial word
        matches.append( v )

        v_clean = clean_word( v )

        for k_2, v_2 in map_a.items():
            if k_2 in processed_keys:
                continue

            v_2_clean = clean_word( v_2 )

            similarity_type = check_similarity( v_clean, v_2_clean )

            if similarity_type == SimilarityType.DUPLICATE:
                # duplicate, just ignore it
                processed_keys[ k ] = 1
            elif similarity_type == SimilarityType.SIMILAR:
                # similar, but not a duplicate, add it
                processed_keys[ k ] = 1
                matches.append( v )
            else:
                # do nothing
                pass

        res_a[ k ] = matches

    return [ res_a, res_b ]

def process( inp_filenames: [str], outp_filenames: [str] ):

    num_req = 0

    map_a = read_map( inp_filenames[0] )
    map_b = read_map( inp_filenames[1] )

    


def main( argv ):

    input_files  = None
    output_files = None
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
