import sys
import os
from parser_kia import Kia

if __name__ == "__main__":

    file = sys.argv[1] 

    parser_kia = Kia()

    parser_kia.parse(file)