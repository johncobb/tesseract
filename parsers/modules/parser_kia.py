import os
import csv
import sys
from decimal import Decimal
from re import sub
from util import ValidateVIN
from parser_base import ParserAbstract

class Kia(ParserAbstract):

    def parse(self, file):

        # Per ISO 3779 valid prefixs for World Manufacturer Identifier
        # and Vehicle Descriptor Section
        # basis: looking for ocr errors that misrepresent portions of the VIN
        # This is done by creating a dictionary of common mistakes and resolution
        # example: record.replace(mfg["kia"]["WMIVDS"][0...n][0], mfg["kia"]["WMIVDS"][0...n][1])
        ocr_common_error = {"WMIVDS": [["SX", "5X"], ["3KP", "5X"]]}


        #print("Running Kia Parser: " + file)

        value = 0.0
        current_principal = 0.0
        current_principal_total = 0

        tess_data = csv.reader(open(file), delimiter=' ',)
        
        #print("Common OCR Errors: ")
        #print(ocr_common_error["WMIVDS"][1])

        for row in tess_data:

            if len(row) > 1:

                if len(row[0]) == 11  and len(row[1]) == 6:
                    
                    record = "{0}{1}".format(row[0], row[1])
                    current_principal = row[2]

                    value = Decimal(sub(r'[^\d.]', '', current_principal))

                    # Remove invalid characters from VIN
                    for key in self.blacklist:
                        record = record.replace(key[0], key[1])

                    current_principal_total += value
                    result = ValidateVIN(record.upper())
                    
                    if result[0]:
                        # we have good data
                        #print record
                        print(record, current_principal, current_principal_total)
                        # validFile.write(recordData + "\n")
                        # encodedFile.write(encodedData + "\n")
                    else:

                        for key in ocr_common_error["WMIVDS"]:
                            record = record.replace(key[0], key[1])

                        result = ValidateVIN(record.upper())

                        if result[0]:
                            print(record, current_principal, current_principal_total)
                            #print record
                        else: 
                            print(record, " invalid", current_principal)
                            #print(record)
                        #invalidFile.write(recordData + "\t" + vinResult[2] + "\n")

        
        #print("Total: ", current_principal_total)
