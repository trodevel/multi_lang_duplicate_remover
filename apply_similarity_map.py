import csv

import sys, getopt
from csv_io import read_map, read_similarity_map, write_map

class SimilarityGroupJoiner:

    def __init__( self, map_a: {}, map_b: {} ):
        self.map_a = map_a
        self.map_b = map_b
        self.processed_keys = None
        self.current_joined_similarity_group = None

    def apply_map( inp: [[]], mapp: [] ) -> []:

        print( f"INFO: joining keys" )

        res = []

        for group in mapp:
            line = []
            if k in group:
                line.append( inp[k] )
            res.append( line )

        return res

def process( inp_filename: str, outp_filename: str, map_filename: str ):

    num_req = 0

    inp  = read_map( inp_filename )
    mapp = read_similarity_map( map_filename )

    res = apply_map( inp, mapp )

    write_map( res, outp_filename )

def main( argv ):

    input_file  = None
    output_file = None
    map_file    = None
    loglevel    = 0

    try:
        opts, args = getopt.getopt(argv,"hHdi:m:l:o:D",["HEADLESS","dry","DEBUG","ifile=","mapfile=","ofile="])
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
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-m", "--mapfile"):
            map_file = arg

    #set_loglevel( loglevel )

    print( f"DEBUG: input file     = {input_file}" )
    print( f"DEBUG: output file    = {output_file}" )
    print( f"DEBUG: map file       = {map_file}" )

    if not input_file:
        print( "FATAL: need input filename" )
        sys.exit( 1 )

    if not output_file:
        print( "FATAL: need output filename" )
        sys.exit( 1 )

    if not map_file:
        print( "FATAL: need map filename" )
        sys.exit( 1 )

    process( input_file, output_file, map_file )

    sys.exit( 0 )

if __name__ == '__main__':
    main( sys.argv[1:] )
