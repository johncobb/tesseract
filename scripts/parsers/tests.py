import unittest
import re
import util

date = '2/29/20'
year = date[-4:]

def check_month(month):
    return month > 0 and month <= 12

def check_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

class TestChecks(unittest.TestCase):
    
    def test_date(self):
        date = input("Enter the date for the vin. ")
        # if re.match(r"^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$", date) \
        # or re.match(r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$", date) \
        # or re.match(r'^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$', date:
        self.assertRegex(date, r'^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
        
    def test_first11(self):
        first11 = input('\nEnter the first 11 characters of the vin. ')
        self.assertTrue(len(first11.strip()) == 11)
        
    def test_last6(self):
        last6 = input('\nEnter the last 6 digits of the vin. ')
        self.assertTrue(len(last6.strip()) == 6 and last6.strip().isdigit())
        
    def test_number(self):
        number = input('\nEnter the balance of the vin. ')
        digi = number.replace('.', '').replace(',', '').replace('€', '').replace('$', '').replace('EUR', '').replace('USD', '').replace('Euro', '').replace('Dollar', '').isdigit()
        self.assertTrue(re.match(r'(\d+([.,]?)\d{0,}([.,]?)\d*(\s*)(\$|€|EUR|USD|Euro|Dollar))|((\$|€|EUR|USD|Euro|Dollar)(\s*)\d+([.,]?\d{0,}([.,]?)\d*))|((\s*)\d+([.,]?\d{0,}([.,]?)\d*))$', number) and digi)
        
    def test_vin_validation(self):
        vin = input('\nEnter the vin you wish to be validated. ')
        valid = util.ValidateVIN(vin)
        self.assertTrue(valid[0])
    
    def test_check_day(self):
        global date, year
        
        
        month = date[0:2]
        day = date[3:5]
        
        if not day.isdigit():
            day = int(day[0])
            
        if not month.isdigit():
            month = int(month[0])
        
        if (year.find('/') > -1 or year.find('.') > -1 or year.find('-') > -1):
            for item in year:
                if item == '/' or item == '.' or item == '-':
                    index = year.index(item) + 1
                    break
        leap_year = check_leap_year(int(year[index:]))
        
        monthlist = {
            '31': [1, 3, 5, 7, 8, 10, 12],
            '30': [4, 6, 9, 11],
            '28': [2]
        }
        
        if not check_month(month):
            return (False, 'Invalid month')
        
        if month in monthlist['31']:
            self.assertTrue(day >= 1 and day <= 31)
        elif month in monthlist['30']:
            self.assertTrue(day >= 1 and day <= 30)
        elif month in monthlist['28'] and not leap_year:
            self.assertTrue(day >= 1 and day <= 28)
        elif month in monthlist['28'] and leap_year:
            self.assertTrue(day >= 1 and day <= 29)
            # self.assertTrue(len(year[index:]) >= 1 and len(year[index:]) <= 4)

    def test_year(self):
        global year
        if (year.find('/') > -1 or year.find('.') > -1 or year.find('-') > -1):
            for item in year:
                if item == '/' or item == '.' or item == '-':
                    index = year.index(item) + 1
                    break
                
        self.assertTrue(len(year[index:]) >= 1 and len(year[index:]) <= 4)

if __name__ == '__main__':
    unittest.main()