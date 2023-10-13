import csv

import sys, getopt

from csv_io import read_similarity_map, write_map

class SimilarityGroupJoiner:

    def __init__( self, map_a: {}, map_b: {} ):
        self.map_a = map_a
        self.map_b = map_b
        self.processed_keys = None
        self.current_joined_similarity_group = None

    def join_groups(self) -> []:

        print( f"INFO: joining keys" )

        res = []

        self.processed_keys = {}

        all_keys = self._get_all_keys()

        for k in all_keys:

            if k in self.processed_keys:
                continue

            self.current_joined_similarity_group = []

            group = self._find_group_by_key( k, True )

            self._process_group_of_map( group, True )

            group = self._find_group_by_key( k, False )

            self._process_group_of_map( group, False )

            res.append( self.current_joined_similarity_group )

        return res

    def _find_group_by_key( self, k: int, is_map_a: bool ) -> []:

        res = []

        map_a_or_b = self.map_a if is_map_a else self.map_b

        for group in map_a_or_b:
            if k in group:
                return group

        return res

    def _get_all_keys( self ) -> []:

        all_keys = {}

        for group in self.map_a:
            for k in group:
                if k not in all_keys:
                    all_keys[k] = 1

        for group in self.map_b:
            for k in group:
                if k not in all_keys:
                    all_keys[k] = 1

        return all_keys.keys()

    def _process_group_of_map( self, group: [], is_map_a: bool ):

        for k in group:
            if k in self.processed_keys:
                continue
            self.current_joined_similarity_group.append( k )
            self.processed_keys[k] = 1
            self._find_similarities_in_map( k, False if is_map_a else True )

    def _find_similarities_in_map( self, k: int, is_map_a: bool ) -> None:

        map_a_or_b = self.map_a if is_map_a else self.map_b

        for group in map_a_or_b:
            if k not in group:
                continue
            for k_2 in group:
                if k_2 in self.processed_keys:
                    continue
                self.current_joined_similarity_group.append( k_2 )
                self.processed_keys[k_2] = 1
                self._find_similarities_in_map( k_2, False if is_map_a else True )

def process( inp_filenames: [str], outp_filename: str ):

    num_req = 0

    map_a = read_similarity_map( inp_filenames[0] )
    map_b = read_similarity_map( inp_filenames[1] )

    r = SimilarityGroupJoiner( map_a, map_b )

    res = r.join_groups()

    write_map( res, outp_filename )

def main( argv ):

    input_files  = []
    output_file = None
    loglevel    = 0

    try:
        opts, args = getopt.getopt(argv,"hHdi:l:o:D",["HEADLESS","dry","DEBUG","ifile=","type=","limit=","ofile="])
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
            output_file = arg

    #set_loglevel( loglevel )

    print( f"DEBUG: num input file = {len(input_files)}" )
    print( f"DEBUG: output file    = {output_file}" )

    if len( input_files ) != 2:
        print( "FATAL: need 2 comma-separated input filenames" )
        sys.exit( 1 )

    if not output_file:
        print( "FATAL: need output filename" )
        sys.exit( 1 )

    process( input_files, output_file )

    sys.exit( 0 )

if __name__ == '__main__':
    main( sys.argv[1:] )
