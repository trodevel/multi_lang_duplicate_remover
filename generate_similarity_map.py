import csv
from enum import Enum
from thefuzz import fuzz

import sys, getopt

from csv_io import read_map, write_map

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

def is_fuzzy_comparison_needed( w_1: str, w_2: str, similarity_pct: int ) -> bool:
    l1 = len( w_1 )
    l2 = len( w_2 )

    if l1 == l2:
        return True

    mx = max( l1, l2 )
    mn = min( l1, l2 )

    ratio = mn * 100 / mx

    if ratio >= similarity_pct:
        return True

    return False

def check_similarity( w_1: str, w_2: str, similarity_pct: int  ) -> SimilarityType:

    if is_fuzzy_comparison_needed( w_1, w_2, similarity_pct ) == False:
        return SimilarityType.DIFFERENT

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

    def __init__( self, map_a: {}, similarity_pct: int ):
        self.map_a = map_a
        self.similarity_pct = similarity_pct
        self.iteration_processed_keys = None

    def remove_duplicates(self) -> [[], []]:

        res = self._refine_and_find_duplicates( self.map_a )

        return res

    def _refine_and_find_duplicates( self, map_raw: {} ) -> []:

        print( f"INFO: refining map" )

        map_refined = refine_map( map_raw )

        print( f"INFO: finding duplicates" )

        res = self._find_duplicates( map_refined )

        return res

    def _find_duplicates( self, map_refined: {} ) -> []:

        res = []

        orig_size = len( map_refined )
        cur_rec = 0

        self.iteration_processed_keys = {}

        while len( map_refined ):

            k = next( iter( map_refined ) )
            v = map_refined[k]

            cur_rec += 1
            cur_size = len( map_refined )

            progress_pct = ( orig_size - cur_size ) * 100 / orig_size

            print( f"DEBUG: processing record {cur_rec}, key {k}, new map size {len( map_refined )}, {progress_pct} %" )

            self._find_duplicates_once( k, v, map_refined )

            if len( self.iteration_matches ) > 1:
                print( f"DEBUG: removing processed {len(self.iteration_matches)} elements" )

            #print( f"DEBUG: iteration processed keys {self.iteration_processed_keys}" )
            for k_m in self.iteration_processed_keys.keys():
                #print( f"DEBUG: removing key {k_m}" )
                del map_refined[k_m]

            res.append( self.iteration_matches )

        return res

    def _find_duplicates_once( self, k: int, v: str, map_refined: {} ) -> []:

        res = []

        self.iteration_matches = []
        self.iteration_processed_keys = { k: 1 }

        # put initial word
        self.iteration_matches.append( k )

        similar_values = self._find_duplicates_for_word( v, map_refined )

        if len( similar_values ):
            print( f"DEBUG: num similar values {len(similar_values)}" )
            for e in similar_values:
                n = self._find_duplicates_for_word( e, map_refined )
                if len( n ):
                    print( f"DEBUG: found {len(n)} additional similar values" )

        res.append( self.iteration_matches )

        return res

    def _find_duplicates_for_word( self, v: str, map_refined: {} ):

        similar_values = []

        for k_2, v_2 in map_refined.items():
            if k_2 in self.iteration_processed_keys:
                continue

            similarity_type = check_similarity( v, v_2, self.similarity_pct )

            if similarity_type == SimilarityType.DUPLICATE:
                # duplicate, just ignore it
                self.iteration_processed_keys[ k_2 ] = 1
                # need to add to similar_values because later join may insert it again as a new key
                similar_values.append( v_2 )
                self.iteration_matches.append( k_2 )
            elif similarity_type == SimilarityType.SIMILAR:
                # similar, but not a duplicate, add it
                self.iteration_processed_keys[ k_2 ] = 1
                similar_values.append( v_2 )
                self.iteration_matches.append( k_2 )
            else:
                # do nothing
                pass

        return similar_values


def process( inp_filename: str, outp_filename: str, similarity_pct: int ):

    num_req = 0

    map_a = read_map( inp_filename )

    r = DuplicateRemover( map_a, similarity_pct )

    res = r.remove_duplicates()

    write_map( res, outp_filename )

def main( argv ):

    input_file  = None
    output_file = None
    loglevel    = 0
    similarity_pct = 85

    try:
        opts, args = getopt.getopt(argv,"hHdi:s:l:o:D",["HEADLESS","dry","DEBUG","ifile=","type=","limit=","ofile="])
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
        elif opt in ("-s", "--sim"):
            similarity_pct = int( arg )

    #set_loglevel( loglevel )

    print( f"DEBUG: input file     = {input_file}" )
    print( f"DEBUG: output file    = {output_file}" )
    print( f"DEBUG: similarity_pct = {similarity_pct}" )

    if not input_file:
        print( "FATAL: need input filename" )
        sys.exit( 1 )

    if not output_file:
        print( "FATAL: need output filename" )
        sys.exit( 1 )

    process( input_file, output_file, similarity_pct )

    sys.exit( 0 )

if __name__ == '__main__':
    main( sys.argv[1:] )
