# pylint: disable=missing-docstring, too-few-public-methods, invalid-name, unused-variable, trailing-whitespace, too-many-locals, bad-whitespace
import math
import sys

def comp_tiles(F, F1, F2, F3):
    MAX_SIZE = 25
    G,G1,G2,G3 = [], [], [], []
    for i in range(0, MAX_SIZE + 1):
        F.append(0)
        F1.append(0)
        F2.append(0)
        F3.append(0)
        G.append(0)
        G1.append(0)
        G2.append(0)
        G3.append(0)
      
    F[0], F[1], F[2] =  1, 2, 11
    F1[0], F1[1], F1[2] =  0, 2, 16
    F2[0], F2[1], F2[2] =  0, 1, 8
    F3[0], F3[1], F3[2] =  0, 0, 4
    G[0], G[1], G[2] =  0, 0, 2
    G1[0], G1[1], G1[2] =  0, 0, 1
    G2[0], G2[1], G2[2] =  0, 0, 1
    G3[0], G3[1], G3[2] =  0, 0, 1

    for n in range(2, MAX_SIZE):
        F[n+1] = 2*F[n] + 7*F[n-1] + 4*G[n]
        F1[n+1] = 2*F1[n] + 2*F[n] + 7*F1[n-1] + 8*F[n-1] + 4*G1[n] + 2*G[n]
        F2[n+1] = 2*F2[n] + F[n] + 7*F2[n-1] + 4*F[n-1] + 4*G2[n] + 2*G[n]
        F3[n+1] = 2*F3[n] + 7*F3[n-1] + 4*F[n-1] + 4*G3[n]+2*G[n]
        test = 2.0 * (n + 1) * F[n+1]
        test1 = F1[n+1] + 2.0*F2[n+1] + 3.0*F3[n+1]
        if math.fabs(test - test1) > 0.000001*test:
            print("mismatch %d: %g != %g\n" %  (n+1, test, test1))

        G[n+1] = 2*F[n-1] + G[n]
        G1[n+1] = 2*F1[n-1] + F[n-1] + G1[n]
        G2[n+1] = 2*F2[n-1] + F[n-1] + G2[n] + G[n]
        G3[n+1] = 2*F3[n-1] + F[n-1] + G3[n]

    return F


def main():
    F,F1,F2,F3 = [], [], [], []
    infile = open(sys.argv[1], "r")
    p = int(infile.readline().split()[0])
    comp_tiles(F, F1, F2, F3)
    for i in range(0, p):
        line_args = infile.readline().split()
        data_set_number = line_args[0]
        n = int(line_args[1])
        if n < 1:
            print("Invalid n value")
        elif n == 1:
            print(data_set_number + " 2 2 1 0")
        else:
            print(data_set_number + " " + str(F[n]) + " " + str(F1[n]) + " " + str(F2[n]) + " " + str(F3[n]))
            

main()


