# pylint: disable=missing-docstring, too-few-public-methods, invalid-name, unused-variable, trailing-whitespace, too-many-locals
import queue as Q
import sys

class Cell:
    def __init__(self, row, col, adj, val='#'):
        self.val = val
        self.row = row
        self.col = col
        self.adj = adj

    def __eq__(self, other):
        return len(self.adj) == len(other.adj)
    def __lt__(self, other):
        return len(self.adj) < len(other.adj)
    def __gt__(self, other):
        return len(self.adj) > len(other.adj)

class Solution:
    def __init__(self, grid=None, to_do=None):
        if to_do is None:
            self.to_do = Q.PriorityQueue()
        if grid is None:
            self.grid = []

def init_solution(s, row, col, infile):

    for i in range(0, row + 2):
        s.grid.append([])

        for j in range(0, col + 2):
            s.grid[i].append(Cell(i, j, set()))

    for i in range(1, row + 1):
        line = infile.readline().split()
        for j in range(1, col + 1):
            s.grid[i][j].val = line[j - 1]

    num_of_blocks = int(infile.readline().split()[0])
    for i in range(0, num_of_blocks):
        blk = set()
        blk_inf = infile.readline().split()
        nsquares = int(blk_inf[0])
        for j in range(1, nsquares + 1):
            blk.add(chr(48 + j))


        for j in range(1, nsquares + 1):
            r = int(blk_inf[j][1])
            c = int(blk_inf[j][3])
            blk.discard(s.grid[r][c].val)
            s.grid[r][c].adj = blk
            if s.grid[r][c].val == '-':
                s.to_do.put(s.grid[r][c])


def adjacent_okay(s, val, r, c):

    for i in range(-1, 2):
        for j in range(-1, 2):
            if s.grid[r + i][c + j].val == val:
                return False
    return True


def attempt(s):
    #print_solution(s)
    #print('\n')
    if s.to_do.empty():
        return True

    curr = s.to_do.get()
    row = curr.row
    col = curr.col
    avail = curr.adj

    for x in avail:
        if adjacent_okay(s, x, row, col):
            curr.adj.discard(x)
            s.grid[row][col].val = x

            if attempt(s):
                return True

            s.grid[row][col].val = '-'
            curr.adj.add(x)

    s.to_do.put(curr)
    return False



def print_solution(sol):
    t = ""
    for i in range(1, len(sol.grid) - 1):
        for j in range(1, len(sol.grid[0]) - 1):
            t += sol.grid[i][j].val + " "
        print(t)
        t = ""


def main():
    infile = open(sys.argv[1], "r")
    p = int(infile.readline().split()[0])

    for i in range(0, p):
        second_line = infile.readline().split()
        print(second_line[0])
        s = Solution()
        init_solution(s, int(second_line[1]), int(second_line[2]), infile)

        if attempt(s):
            print_solution(s)
        else:
            print("No Solution.")

main()
