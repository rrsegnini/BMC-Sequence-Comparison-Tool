from SequenceComparisonAlgorithms import *
from Lyrics import *
import _sqlite3 as sql




def main():
    print(NeedlemanWunsch("ABCD","AABB",1,-1,-2))

main()
