import sys
import hashlib
import re

vinRegex = re.compile(r"^(?P<wmi>[A-HJ-NPR-Z\d]{3})(?P<vds>[A-HJ-NPR-Z\d]{5})(?P<check>[\dX])(?P<vis>(?P<year>[A-HJ-NPR-Z\d])(?P<plant>[A-HJ-NPR-Z\d])(?P<seq>[A-HJ-NPR-Z\d]{6}))$")
transliterationString = "0123456789.ABCDEFGH..JKLMN.P.R..STUVWXYZ"
valWeights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

def calculateCheckDigit(vin):
     return sum([x[0] * x[1] for x in zip([transliterationString.find(c) % 10 for c in vin], valWeights)]) % 11


def ValidateVIN(vin, many=False):
    if many:
        results = []
        for v in vin:
            results.append(ValidateVIN(v))
        return results

    else:
        if len(vin) != 17:
            return (False, vin, "Invalid Length")

        for c in vin:
            if c not in transliterationString:
                return (False, vin, "Invalid Character")

        if vin[8] not in "0123456789X":
            return (False, vin, "Invalid Checksum Character")

        if vin[8] == "X":
            cd = 10
        else:
            cd = int(vin[8])

        if  calculateCheckDigit(vin) == cd:
            return (True, vin, "Valid VIN")
        else:
            return (False, vin, "Invalid Checksum calculation")


class ISO3779_VIN():

    def __init__(self, vin):
        self.vin = vin
        re_match = vinRegex.match(vin)
        if re_match:
            self._match_dict = re_match.groupdict()
            for k,v in self._match_dict.items():
                setattr(self, k, v)
            self._validation = ValidateVIN(vin)
            self.is_valid = self._validation[0]
        else:
            self.is_valid = False
            self._match_dict = {}
            self._validation = (None, None, None)

    def __repr__(self):
        return str(self._match_dict)

if __name__ == "__main__":
    print(ValidateVIN(sys.argv[1]))