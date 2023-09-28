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

def write_map( m: {}, filename: str ) -> None:

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

def check_similarity( w_1: str, w_2: str, similarity_pct: int  ) -> SimilarityType:
    r = fuzz.ratio( w_1, w_2 )

    if r >= 95:
        #print( f"DEBUG: DUP - w_1 '{w_1}', w_2 '{w_2}'" )
        return SimilarityType.DUPLICATE
    elif r >= similarity_pct:
        #print( f"DEBUG: SIM - w_1 '{w_1}', w_2 '{w_2}'" )
        return SimilarityType.SIMILAR

    #print( f"DEBUG: DIF - w_1 '{w_1}', w_2 '{w_2}'" )
    return SimilarityType.DIFFERENT

class DuplicateRemover:

    def __init__( self, map_a: {}, map_b: {}, similarity_pct: int ):
        self.map_a = map_a
        self.map_b = map_b
        self.similarity_pct = similarity_pct
        self.map_a_refined = None
        self.map_b_refined = None
        self.processed_keys = None

    def remove_duplicates(self) -> [{}, {}]:

        res_a = {}
        res_b = {}

        print( f"DEBUG: refining maps" )

        self.map_a_refined = refine_map( self.map_a )
        self.map_b_refined = refine_map( self.map_b )

        self.processed_keys = {}

        res_a = self._find_duplicates( self.map_a_refined )
        res_b = self._find_duplicates( self.map_b_refined )

        return [ res_a, res_b ]


    def _find_duplicates( self, map_refined: {} ):

        res = {}

        num_rec = len( map_refined )
        cur_rec = 0

        for k, v in map_refined.items():

            cur_rec += 1

            if k in self.processed_keys:
                continue

            print( f"DEBUG: processing record {cur_rec}/{num_rec}, num processed keys {len(self.processed_keys)}" )

            self.processed_keys[ k ] = 1

            self.matches = []

            # put initial word
            self.matches.append( k )

            similar_values = self._find_duplicates_for_word( v, map_refined )

            if len( similar_values ):
                print( f"DEBUG: num similar values {len(similar_values)}" )
                for e in similar_values:
                    n = self._find_duplicates_for_word( e, map_refined )
                    print( f"DEBUG: found {len(n)} additional similar values" )

            res[ k ] = self.matches

        return res

    def _find_duplicates_for_word( self, v: str, map_refined: {} ):

        similar_values = []

        for k_2, v_2 in map_refined.items():
            if k_2 in self.processed_keys:
                continue

            similarity_type = check_similarity( v, v_2, self.similarity_pct )

            if similarity_type == SimilarityType.DUPLICATE:
                # duplicate, just ignore it
                self.processed_keys[ k_2 ] = 1
            elif similarity_type == SimilarityType.SIMILAR:
                # similar, but not a duplicate, add it
                self.processed_keys[ k_2 ] = 1
                similar_values.append( v_2 )
                self.matches.append( k_2 )
            else:
                # do nothing
                pass

        return similar_values


def process( inp_filenames: [str], outp_filenames: [str], similarity_pct: int ):

    num_req = 0

    map_a = read_map( inp_filenames[0] )
    map_b = read_map( inp_filenames[1] )

    r = DuplicateRemover( map_a, map_b, similarity_pct )

    res_a, res_b = r.remove_duplicates()

    write_map( res_a, outp_filenames[0] )
    write_map( res_b, outp_filenames[1] )

def main( argv ):

    input_files  = []
    output_files = []
    loglevel    = 0
    similarity_pct = 85

    try:
        opts, args = getopt.getopt(argv,"hHdi:s:l:o:D",["HEADLESS","dry","DEBUG","ifile=","type=","limit=","offset="])
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
        elif opt in ("-s", "--sim"):
            similarity_pct = int( arg )

    #set_loglevel( loglevel )

    print( f"DEBUG: num input file = {len(input_files)}" )
    print( f"DEBUG: similarity_pct = {similarity_pct}" )

    if len( input_files ) != 2:
        print( "FATAL: need 2 comma-separated input filenames" )
        sys.exit( 1 )

    if len( output_files ) != 2:
        print( "FATAL: need 2 comma-separated output filenames" )
        sys.exit( 1 )

    process( input_files, output_files, similarity_pct )

    sys.exit( 0 )

if __name__ == '__main__':
    main( sys.argv[1:] )
