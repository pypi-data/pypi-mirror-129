#!python
'''
Takes a database as argument 1 and an output for the .tsv as argument 2.
Calculates basic genome statistics.
'''

import sys, os, pandas as pd, multiprocessing as mp, copy
from mycotools.lib.dbtools import db2df, log_editor
from mycotools.lib.biotools import fa2dict
from mycotools.lib.kontools import formatPath, eprint


def calcMask( contig_list ):

    seq = ''.join([x['sequence'] for x in contig_list])
    mask = seq.count('a')
    mask += seq.count('t')
    mask += seq.count('g')
    mask += seq.count('c')

    return mask


def sortContigs( assembly_path ):
    '''Imports fasta, creates a list of dicts for each contig length and its name.
       Sorts the list in descending order by length'''

    contigList = []
    assembly = fa2dict( assembly_path )
    for contig in assembly:
        contigList.append( {
            'len': len(assembly[contig]['sequence']), 
            'name': contig, 
            'sequence': str(assembly[contig]['sequence'])
        } )

    sortedList = sorted(contigList, key = lambda i: i['len'], reverse = True)

    return sortedList


def n50l50( sortedContigs ):
    '''Calculates contigs greater than 1000 bp, the total length excluding 1000 bp contigs.
       Then caculates l50, n50, largest contig, total contigs, shortest contig, and l50%.
       Returns a dictionary of the results.'''

    pass_fa = []
    total, total1000, bp1000, gc, gc1000, gctot, gctot1000 = 0, 0, 0, 0, 0, 0, 0
    for contig in sortedContigs:
        total += contig['len']
        gc += contig['sequence'].lower().count( "g" ) + contig['sequence'].lower().count( 'c' )
        gctot += contig['sequence'].lower().count( "g" ) + contig['sequence'].lower().count( 'c' ) + \
           contig['sequence'].lower().count( 'a' ) + contig['sequence'].lower().count( 't' ) 
        if contig['len'] >= 1000:
            gc1000 += contig['sequence'].lower().count( "g" ) + contig['sequence'].lower().count( 'c' )
            gctot1000 += contig['sequence'].lower().count( "g" ) + contig['sequence'].lower().count( 'c' ) + \
                contig['sequence'].lower().count( 'a' ) + contig['sequence'].lower().count( 't' ) 
            total1000 += contig['len']
            bp1000 += 1
            pass_fa.append( contig )


    out = {}
    count50, count, check = 0, 0, 0
    for contig in sortedContigs:
        count50 += contig['len']
        count += 1
        if count50 >= total1000/2:
            if contig['len'] >= 1000 and check != 1:
                out['n50-1000bp'] = int(contig['len'])
                out['l50-1000bp'] = int(count)
                out['l50%-1000bp'] = out['l50-1000bp']/int(bp1000)
                check = 1
            if count50 >= total/2:
                out['n50'] = int(contig['len'])
                out['l50'] = int(count)
                break

    try:
        out['l50%'] = out['l50']/len(sortedContigs)
        out['largest_contig'] = sortedContigs[0]['len']
        out['shortest_contig'] = sortedContigs[-1]['len']
        out['contigs'] = len(sortedContigs)
        out['contigs-1000bp'] = bp1000
        out['assembly_len'] = int(total)
        out['assembly_len-1000bp'] = int(total1000)
        out['gc'] = float(gc/gctot)
        out['gc-1000bp'] = float(gc1000/gctot1000)
        if 'n50-1000bp' not in out:
            out['n50-1000bp'] = 'na'
            out['l50-1000bp'] = 'na'
        maskCount = calcMask( sortedContigs )
        maskCount1000 = calcMask( pass_fa )
        out['mask%'] = maskCount / int( total ) * 100
        out['mask%-1000bp'] = maskCount1000 / int( total1000) * 100
        
    except KeyError:
        out = {}


    return out

def mngr(assembly_path, ome):
    sortedContigs = sortContigs(assembly_path)
    calcs = n50l50(sortedContigs)
    return ome, tuple([(x, calcs[x]) for x in calcs])

def main():

    usage = '\nUSAGE: assembly statistics\tAssembly `fasta` or mycotoolsDB, optional output file if using database\n'
    if len(sys.argv) < 2:
        print( usage , flush = True)
        sys.exit( 1 )

    stats = {}

    if formatPath(sys.argv[1]).endswith('.db'):
        log_path = None
        head = '#ome\tn50-1000bp\tl50-1000bp\tl50%-1000bp\tn50\tl50\tl50%\tlargest_contig\tshortest_contig\tcontigs' + \
            '\tcontigs-1000bp\tassembly_len\tassembly_len-1000bp\tgc\tgc-1000bp\tmask%\tmask%-1000bp'

        if len(sys.argv) > 2:
            log_path = sys.argv[2]
            if not os.path.isfile( log_path ):
                with open( log_path, 'w' ) as log_open:
                    log_open.write( head )

        db = db2df(sys.argv[1])

        cmds = []
        for i, row in db.iterrows():
            if not pd.isnull(row['assembly']):
                cmds.append((formatPath('$MYCOFNA/' + row['assembly']), copy.deepcopy(row['internal_ome'])))
        with mp.Pool(processes=os.cpu_count()) as pool:
            results = pool.starmap(mngr, cmds)

        if log_path:
            for res in results:
                ome, calcs = res[0], res[1]
                if calcs:
                    calcs = {x[0]: x[1] for x in calcs}
               
                    log_editor( log_path, ome, ome + '\t' + str(calcs['n50-1000bp']) + '\t' + \
                        str(calcs['l50-1000bp']) + '\t' + str(calcs['l50%-1000bp']) + '\t' + str(calcs['n50']) + '\t' + \
                        str(calcs['l50']) + '\t' + str(calcs['l50%']) + '\t' + str(calcs['largest_contig']) + '\t' + \
                        str(calcs['shortest_contig']) + '\t' + str(calcs['contigs']) + '\t' + str(calcs['contigs-1000bp']) + \
                        '\t' + str(calcs['assembly_len']) + '\t' + str(calcs['assembly_len-1000bp']) + '\t' + str(calcs['gc']) + \
                        '\t' + str(calcs['gc-1000bp']) + '\t' + str(calcs['mask%']) + '\t' + str(calcs['mask%-1000bp']))
                else:
                    eprint('\t\tERROR:\t' + ome, flush = True)
        else:
            print(head, flush = True)
            for res in results:
                ome, calcs = res[0], res[1]
                if calcs:
                    calcs = {x[0]: x[1] for x in calcs}
                    print(ome + '\t' + str(calcs['n50-1000bp']) + '\t' + \
                        str(calcs['l50-1000bp']) + '\t' + str(calcs['l50%-1000bp']) + '\t' + str(calcs['n50']) + '\t' + \
                        str(calcs['l50']) + '\t' + str(calcs['l50%']) + '\t' + str(calcs['largest_contig']) + '\t' + \
                        str(calcs['shortest_contig']) + '\t' + str(calcs['contigs']) + '\t' + str(calcs['contigs-1000bp']) + \
                        '\t' + str(calcs['assembly_len']) + '\t' + str(calcs['assembly_len-1000bp']) + '\t' + str(calcs['gc']) + \
                        '\t' + str(calcs['gc-1000bp']) + '\t' + str(calcs['mask%']) + '\t' + str(calcs['mask%-1000bp']))
                else:
                    eprint('\t\tERROR:\t' + ome, flush = True)


    else:

        sortedContigs = sortContigs( sys.argv[1] )
        calculations = n50l50( sortedContigs )
        if calculations:
            stats[ os.path.basename( os.path.abspath( sys.argv[1] )) ] = n50l50( sortedContigs )
        else:
            eprint('\tERROR:\t' + sys.argv[1] , flush = True)

        for stat in stats:
            if stats[stat]['shortest_contig'] >= 1000:
                stats[stat] = { 
                    info: stats[stat][info]  for info in stats[stat] if '1000bp' not in info 
                }
            for info in stats[stat]:
                print( '{:<25}'.format( info.upper() + ':' ) + str( stats[stat][info] ) , flush = True)
            
#        out_df = pd.DataFrame.from_dict( stats, orient = 'index')
 #       out_df.to_csv( sys.argv[2], sep ='\t' )

    sys.exit(0)

if __name__ == '__main__':
    main()

