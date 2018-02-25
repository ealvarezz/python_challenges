# pylint: disable=missing-docstring, too-few-public-methods, invalid-name, unused-variable, trailing-whitespace, too-many-locals, trailing-newlines, no-else-return, too-many-branches, too-many-statements, too-many-nested-blocks, line-too-long,bad-whitespace, too-many-return-statements, too-many-instance-attributes, too-many-arguments 
import sys
import math

ALL_MASK = 0x1ff
valid_masks = [0, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x100]
constraints = [[0 for i in range(9)] for j in range(15)]

class _search_state_:
    def __init__(self, avail_mask=None, row_avail_counts=None,
                 col_avail_counts=None, val_set=None, box_avail_counts=None):

        if avail_mask is None:
            self.avail_mask = [[ALL_MASK for i in range(9)] for j in range(9)]

        if row_avail_counts is None:
            self.row_avail_counts = [[9 for i in range(9)] for j in range(9)]

        if col_avail_counts is None:
            self.col_avail_counts = [[9 for i in range(9)] for j in range(9)]

        if val_set is None:
            self.val_set = [[0 for i in range(9)] for j in range(9)]

        if box_avail_counts is None:
            self.box_avail_counts = [[[9 for i in range(9)] for j in range(3)] for z in range(3)]

states = [_search_state_() for i in range(81)]

# In this case prow will be equal to constraints[5*i*2*j] or +1, do not include
# the zero since we want to pass the list, not the value
def scan_convert(prow, infile):

    c = 0
    cons_list = infile.readline().split()[0]
    for cons in cons_list:
        if cons == '<':
            prow[c] = -1
        elif cons == '=':
            prow[c] = 0
        elif cons == '>':
            prow[c] = 1
        else:
            return c
        c += 1

    return c


def scan_constraints(infile):
    for i in range(3):
        for j in range(3):
            #print(5*i*2*j)
            n = scan_convert(constraints[5*i+2*j], infile)
            if n != 6:
                print("Supposed to scan 6")
            if j < 2:
                n = scan_convert(constraints[5*i+2*j+1], infile)
                if n != 9:
                    print("Supposed to scan 9")
    return 0


def check_equal(base_mask, chkmask):

    result = 0
    if valid_masks[5] & base_mask:
        result |= valid_masks[5]

    for i in range(1, 10):
        if ((valid_masks[i] & chkmask) == 0) and (valid_masks[10-i] & base_mask):
            result |= valid_masks[10-i]
    return result


def check_less(base_mask, chkmask):

    result = 0
    if valid_masks[9] & base_mask:
        result |= valid_masks[9]

    for i in range(1, 9):
        if (valid_masks[i] & chkmask) != 0:
            break
        elif valid_masks[9-i] & base_mask:
            result |= valid_masks[9-i]
    return result


def check_greater(base_mask, chkmask):
    result = 0

    if valid_masks[1] & base_mask:
        result |= valid_masks[1]

    for i in range(9, 2, -1):
        if (valid_masks[i] & chkmask) != 0:
            break
        elif valid_masks[11-i] & base_mask:
            result |= valid_masks[11-i]
    return result


def check_constraint(constraint, base_mask, chkmask):
    if constraint < 0:
        return check_less(base_mask, chkmask)
    elif constraint > 0:
        return check_greater(base_mask, chkmask)
    else:
        return check_equal(base_mask, chkmask)


def check_constraints(pss):
    change_count = 1
    scan_count = 0

    while change_count > 0:
        scan_count += 1
        change_count = 0
        base_cons_row = 0
        for row in range(9):
            base_cons_col = 0
            for col in range(9):
                if pss.val_set[row][col] == 0:
                    base_mask = pss.avail_mask[row][col]
                    tot_result = 0

                    if (col % 3) != 0:
                        chkmask = pss.avail_mask[row][col-1]
                        result_mask = check_constraint(constraints[base_cons_row][base_cons_col-1], base_mask, chkmask)
                        if result_mask != 0:
                            base_mask &= ~result_mask
                            change_count += 1
                            tot_result |= result_mask

                    if (col % 3) != 2:
                        chkmask = pss.avail_mask[row][col+1]
                        result_mask = check_constraint(constraints[base_cons_row][base_cons_col], base_mask, chkmask)
                        if result_mask != 0:
                            base_mask &= ~result_mask
                            change_count += 1
                            tot_result |= result_mask

                    if (row % 3) != 0:
                        chkmask =  pss.avail_mask[row-1][col]
                        result_mask = check_constraint(constraints[base_cons_row-1][col], base_mask, chkmask)
                        if result_mask != 0:
                            base_mask &= ~result_mask
                            change_count += 1
                            tot_result |= result_mask


                    if (row % 3) != 2:
                        chkmask = pss.avail_mask[row+1][col]
                        result_mask = check_constraint(constraints[base_cons_row+1][col], base_mask, chkmask)
                        if result_mask != 0:
                            base_mask &= ~result_mask
                            change_count += 1
                            tot_result |= result_mask

                    if base_mask == 0:
                        return -1
                    pss.avail_mask[row][col] = base_mask
                    if tot_result != 0:

                        for i in range(9):
                            if valid_masks[i] & tot_result:
                                pss.col_avail_counts[col][i-1] -= 1
                                pss.row_avail_counts[row][i-1] -= 1
                                pss.box_avail_counts[math.floor(row/3)][math.floor(col/3)][i-1] -= 1

                if (col % 3) != 2:
                    base_cons_col += 1

            if (row % 3) != 2:
                base_cons_row += 2
            else:
                base_cons_row += 1

    return 0

STYP_ROW = 1
STYP_COL = 2
STYP_BOX = 3

class _solve_data_:
    def __init__(self, solve_type=0, solve_val=0, solve_row=0, solve_col=0,solve_cnt=0, solve_index=0,test_row=0, test_col=0):
        self.solve_type = solve_type
        self.solve_val = solve_val
        self.solve_row = solve_row
        self.solve_col = solve_col
        self.solve_cnt = solve_cnt
        self.solve_index = solve_index
        self.test_row = test_row
        self.test_col = test_col

def get_solve_step(pss, psd):
    psd.solve_cnt = 10
    for i in range(9):
        for j in range(9):
            if pss.row_avail_counts[i][j] < psd.solve_cnt:
                psd.solve_cnt = pss.row_avail_counts[i][j]
                psd.solve_type = STYP_ROW
                psd.solve_row = i
                psd.solve_val = j + 1

    for i in range(9):
        for j in range(9):
            if pss.col_avail_counts[i][j] < psd.solve_cnt:
                psd.solve_cnt = pss.col_avail_counts[i][j]
                psd.solve_type = STYP_COL
                psd.solve_col = i
                psd.solve_val = j + 1

    for i in range(3):
        for j in range(3):
            for k in range(9):
                if pss.box_avail_counts[i][j][k] < psd.solve_cnt:
                    psd.solve_cnt = pss.box_avail_counts[i][j][k]
                    psd.solve_type = STYP_BOX
                    psd.solve_row = i
                    psd.solve_col = j
                    psd.solve_val = k + 1

    if psd.solve_cnt == 0:
        return -1
    else:
        return 0


def find_next_test(pss, psd):
    starti = startj = 0
    mask = valid_masks[psd.solve_val]
    if psd.solve_index >= psd.solve_cnt:
        return -1

    if psd.solve_type == STYP_ROW:
        if psd.solve_index == 0:
            startj = 0
        else:
            startj = psd.test_col + 1
        i = psd.solve_row
        for j in range(startj, 9):
            if pss.avail_mask[i][j] & mask:
                psd.test_col = j
                psd.test_row = i
                psd.solve_index += 1
                return 0

        return -1

    elif psd.solve_type == STYP_COL:
        if psd.solve_index == 0:
            starti = 0
        else:
            starti = psd.test_row + 1
        j = psd.solve_col
        for i in range(starti, 9):
            if pss.avail_mask[i][j] & mask:
                psd.test_col = j
                psd.test_row = i
                psd.solve_index += 1
                return 0

        return -1

    elif psd.solve_type == STYP_BOX:
        if psd.solve_index == 0:
            starti = 0
            startj = 0
        else:
            starti = psd.test_row - 3*psd.solve_row
            startj = psd.test_col+1 - 3*psd.solve_col
        for i in range(starti, 3):
            for j in range(startj, 3):
                if pss.avail_mask[i + 3*psd.solve_row][j + 3*psd.solve_col] & mask:
                    psd.test_col = j + 3*psd.solve_col
                    psd.test_row = i + 3*psd.solve_row
                    psd.solve_index += 1
                    return 0
        return -1

    else:
        print("Bad solve type" + str(psd.solve_type))
        return -1


def apply_choice(pss, row, col, val):
    mask = valid_masks[val]
    if pss.val_set[row][col] != 0:
        print("Apply choice something went wrong at the beggining")
        return -1
    pss.val_set[row][col] = val
    boxr = math.floor(row/3)
    boxc = math.floor(col/3)
    for j in range(9):
        if pss.avail_mask[row][j] & mask:
            pss.box_avail_counts[boxr][math.floor(j/3)][val-1] -= 1
            pss.col_avail_counts[j][val-1] -= 1
        pss.avail_mask[row][j] &= ~mask

    for i in range(9):
        if pss.avail_mask[i][col] & mask:
            pss.box_avail_counts[math.floor(i/3)][boxc][val-1] -= 1
            pss.row_avail_counts[i][val-1] -= 1
        pss.avail_mask[i][col] &= ~mask

    boxr = math.floor(row/3)
    boxc = math.floor(col/3)
    for i in range(3*boxr, 3*(boxr+1)):
        for j in range(3*boxc, 3*(boxc+1)):
            if pss.avail_mask[i][j] & mask:
                pss.col_avail_counts[j][val-1] -= 1
                pss.row_avail_counts[i][val-1] -= 1
            pss.avail_mask[i][j] &= ~mask

    for i in range(1, 10):
        if (i != val) and ((pss.avail_mask[row][col] & valid_masks[i]) != 0):
            pss.box_avail_counts[math.floor(row/3)][math.floor(col/3)][i-1] -= 1
            pss.col_avail_counts[col][i-1] -= 1
            pss.row_avail_counts[row][i-1] -= 1

    pss.avail_mask[row][col] = mask
    pss.row_avail_counts[row][val-1] = 32
    pss.col_avail_counts[col][val-1] = 32
    pss.box_avail_counts[boxr][boxc][val-1] = 32

    return 0


def solve(level):
    pssnxt = _search_state_()
    pss = states[level]
    sd = _solve_data_()

    if get_solve_step(pss, sd) != 0:
        return -1

    sd.solve_index = 0
    while find_next_test(pss, sd) == 0:
        if level == 80:
            pss.val_set[sd.test_row][sd.test_col] = sd.solve_val
            return 0
        else:

            states[level + 1] = pss
            pssnxt = states[level + 1]

            if apply_choice(pssnxt, sd.test_row, sd.test_col, sd.solve_val) == 0:
                if check_constraints(pssnxt) == 0:
                    if solve(level + 1) == 0:
                        for i in range(9):
                            for j in range(9):
                                pss.val_set[i][j] = pssnxt.val_set[i][j]
                        return 0
            else:
                print("(solve) Something went wrong with the levels")

    return -1


def main():

    infile = open(sys.argv[1], "r")
    p = int(infile.readline().split()[0])

    for curprob in range(0, p):
        index = infile.readline().split()[0]
        ret = scan_constraints(infile)
        if check_constraints(states[0]) != 0:
            print("Wack")
        solve(0)
        print(index)
        for i in range(9):
            for j in range(9):
                print(str(states[0].val_set[i][j]) + " ", end='')
            print()

    return 0

main()
