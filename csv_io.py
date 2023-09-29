import csv

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
