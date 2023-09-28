import csv

import sys, getopt

def read_similarity_map( filename: str ) -> []:

    res = []

    with open( filename ) as csvfile:
        reader = csv.reader( csvfile, delimiter=';' )
        for row in reader:
            int_row = []
            for i in row:
                int_row.append( int( i ) )

            res.append( int_row )

    print( f"INFO: read {len(res)} records from {filename}" )

    return res

def write_map( m: [], filename: str ) -> None:

    writer = csv.writer( open( filename, "w" ), delimiter=';', lineterminator='\n' )

    for e in m:
        writer.writerow( ( e ) )

    print( f"INFO: wrote {len(m)} records to {filename}" )

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

        for group in self.map_a:

            self.current_joined_similarity_group = []

            self._process_group_of_map_a( group )

            res.append( self.current_joined_similarity_group )

        return res

    def _process_group_of_map_a( self, group: [] ):

        for k in group:
            if k in self.processed_keys:
                continue
            self.current_joined_similarity_group.append( k )
            self.processed_keys[k] = 1
            self._find_similarities_in_map( k, False )

    def _process_group_of_map_b( self, group: [] ):

        for k in group:
            if k in self.processed_keys:
                continue
            self.current_joined_similarity_group.append( k )
            self.processed_keys[k] = 1
            self._find_similarities_in_map( k, True )

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
