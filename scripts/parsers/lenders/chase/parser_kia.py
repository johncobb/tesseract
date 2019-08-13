import os
import csv
import sys
from decimal import Decimal
from re import sub
from parsers.util import ValidateVIN
from parsers.parser_base import ParserAbstract

class Kia(ParserAbstract):

    def removeLowerCase(self, data):
        allUpper = ""

        for c in data:
            if c.isnumeric():
                allUpper += c

                continue
            if (c.isupper()):
                allUpper += c
        
        return allUpper

    def parse(self, file):

        #print("Running Kia Parser: " + file)

        tess_data = csv.reader(open(file), delimiter=' ',)
        
        #print("Common OCR Errors: ")
        #print(ocr_common_error["WMIVDS"][1])

        for row in tess_data:

            if len(row) > 1:

                wmivds = row[0]
                serial = row[1]
                current_principal = row[2]

                if len(row[0]) == 11  and len(row[1]) == 6:
                    self.parseReord(wmivds, serial, current_principal)
                else:
                    wmivds = self.removeLowerCase(wmivds)
                    serial = self.removeLowerCase(serial)
                    self.parseReord(wmivds, serial, current_principal)
                    
    def fixVIN(self, vin='', first11='', last6=''):
        ocr_common_error = {"WMIVDS": [["SX", "5X"], ["3KP", "5X"]]}
        
        
        if not vin:
            if not first11 or not last6:
                return (False, 'Error: Vin, first 11 characters or last 6 characters must be passed in.', '')
            
            vin = first11 + str(last6)
        
        vin = self.removeLowerCase(vin)
        if not len(vin) == 17:
            return (False, 'Vin must be length 17', vin)
        
        for key in self.blacklist:
            vin = vin.replace(key[0], key[1])
        
        result = ValidateVIN(vin)
        
        if result[0]:
            return (True, 'Passed', vin)
        else:
            for key in ocr_common_error['WMIVDS']:
                vin = vin.replace(key[0], key[1])
            
            result = ValidateVIN(vin)
            
            if result[0]:
                return (True, 'Passed', vin)
            
            return (False, 'Error: Invalid', vin)

    def parseReord(self, wmivds, serial, current_principal):

        # Per ISO 3779 valid prefixs for World Manufacturer Identifier
        # and Vehicle Descriptor Section
        # basis: looking for ocr errors that misrepresent portions of the VIN
        # This is done by creating a dictionary of common mistakes and resolution
        # example: record.replace(mfg["kia"]["WMIVDS"][0...n][0], mfg["kia"]["WMIVDS"][0...n][1])
        ocr_common_error = {"WMIVDS": [["SX", "5X"], ["3KP", "5X"]]}

        value = 0.0
        current_principal = 0.0
        current_principal_total = 0

        record = "{0}{1}".format(wmivds, serial)
        current_principal = current_principal

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
        
        #print("Total: ", current_principal_total)