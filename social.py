# pylint: disable=missing-docstring, too-few-public-methods, invalid-name, unused-variable, trailing-whitespace, too-many-locals, bad-whitespace, trailing-newlines, line-too-long
import sys
import math

MAX_NODES = 20
MAX_QUERYS = 10
query1 = [0 for i in range(MAX_QUERYS)]
query2 = [0 for i in range(MAX_QUERYS)]

def adjacent_init(nnodes, nqueries):
    Adjacent = []

    for i in range(0, nnodes + 1):
        Adjacent.append([])
        for j in range(0, nnodes + nqueries):
            Adjacent[i].append(0.0)

    for i in range(0, nnodes):
        Adjacent[nnodes][i] = 1.0

    return Adjacent


def scan_edge_data(Adjacent, pb):
    edge_info = pb.readline().split()
    #print(edge_info)
    node = int(edge_info[0])
    count = int(edge_info[1])
    #print(count)
    Adjacent[node-1][node-1] += count

    for i in range(0, count):
        #print(int(edge_info[i+2]))
        val = int(edge_info[i+2])
        Adjacent[node-1][val-1] = -1.0
        Adjacent[val-1][node-1] = -1.0
        Adjacent[val-1][val-1] += 1.0

    return count


def find_max_rows(Adjacent, nnodes, currow):

    _max = math.fabs(Adjacent[currow][currow])
    maxrow = currow
    for i in range(currow + 1, nnodes + 1):
        tmp = math.fabs(Adjacent[i][currow])
        if tmp > _max:
            _max = tmp
            maxrow = i

    return maxrow


def swap_rows(Adjacent, maxrow, currow, nnodes, nqueries):
    ncols = nnodes + nqueries
    for i in range(0, ncols):
        tmp = Adjacent[currow][i]
        Adjacent[currow][i] = Adjacent[maxrow][i]
        Adjacent[maxrow][i] = tmp


def eliminate(Adjacent, currow, nrows, ncols):
    for i in range(0, nrows):
        if i == currow:
            continue
        factor = Adjacent[i][currow]
        for j in range(currow, ncols):
            Adjacent[i][j] -= factor*Adjacent[currow][j]

    return 0


def dump_matrix(Adjacent, nrows, ncols):
    for i in range(0, nrows):
        for j in range(ncols):
            print("%.2lf " % (Adjacent[i][j]), end='')
        print()
    print()


def solve_matrix(Adjacent, nnodes, nqueries):

    ncols = nnodes + nqueries
    nrows = nnodes + 1

    for currow in range(0, nnodes):
        maxrow = find_max_rows(Adjacent, nnodes, currow)
        if maxrow != currow:
            swap_rows(Adjacent, maxrow, currow, nnodes, nqueries)
        pivot = Adjacent[currow][currow]
        if math.fabs(pivot) < 0.001:
            return -1
        pivot = 1.0/pivot
        for i in range(currow, ncols):
            Adjacent[currow][i] *= pivot
        eliminate(Adjacent, currow, nrows, ncols)

    return 0


def main():

    infile = open(sys.argv[1], "r")
    nprob = int(infile.readline().split()[0])
    for cur in range(0, nprob):

        dataset_info = infile.readline().split()
        nnodes = int(dataset_info[1])
        nqueries = int(dataset_info[2])
        nedges = int(dataset_info[3])
        Adjacent = adjacent_init(nnodes, nqueries)
        edgecnt = edgelines = 0

        while edgecnt < nedges:
            edge_count = scan_edge_data(Adjacent, infile)
            edgelines += 1
            edgecnt += edge_count

        for i in range(0, nqueries):
            query_data = infile.readline().split()
            queryno = int(query_data[0])
            query1[i] = int(query_data[1])
            query2[i] = int(query_data[2])
            Adjacent[query1[i]-1][nnodes + i] = 1.0
            Adjacent[query2[i]-1][nnodes + i] = -1.0

        solve_matrix(Adjacent, nnodes, nqueries)
        print(cur + 1, end='')
        for i in range(0, nqueries):
            dist = math.fabs(Adjacent[query1[i]-1][nnodes + i] - Adjacent[query2[i]-1][nnodes + i])
            print(" %.3lf" % (dist), end='')
        print()


main()
