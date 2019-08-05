import unittest
import re
import util

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
        
        self.assertTrue(re.match(r'^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}', number))
       # 5XYPK4A53KG
       # 448403
       # 49,984.00
    def test_vin_validation(self):
        vin = input('\nEnter the vin you wish to be validated. ')
        valid = util.ValidateVIN(vin)
        self.assertTrue(valid[0])
        
if __name__ == '__main__':
    unittest.main()