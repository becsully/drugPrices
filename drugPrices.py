from __future__ import division
import csv
import time
from pprint import pprint


class Drug(object):
    def __init__(self, name, fda_id, unit, otc, b_or_g, source):
        self.name = name
        self.id = fda_id
        self.prices = {}
        self.unit = unit
        self.otc = otc
        self.b_or_g = b_or_g
        self.lowest = ("20500101", 1000000.0)
        self.highest = ("20000101", 0.0)
        self.current = ("19000101", 0.0)
        self.oldest = ("20500101", 0.0)
        self.change = 0
        self.vendor = "(None listed)"
        self.package = "(None listed)"
        self.source = source

    def add_price(self, datestr, price): #date str formatted YYYYMMDD, float
        self.prices[datestr] = float(price)
        Drug.update_prices(self)

    def add_vendor(self, vendor):
        self.vendor = vendor

    def add_package(self, package):
        self.package = package

    def update_prices(self):
        for date in self.prices:
            if date > self.current[0]:
                self.current = (date, self.prices[date])
            if date < self.oldest[0]:
                self.oldest = (date, self.prices[date])
            if self.prices[date] < self.lowest[1]:
                lowest = self.prices[date]
                self.lowest = (date, lowest)
            if self.prices[date] > self.highest[1]:
                highest = self.prices[date]
                self.highest = (date, highest)
        try:
            self.change = ( self.current[1] / self.oldest[1] ) - 1
        except ZeroDivisionError:
            pass

    def printer(self):
        print "Name: " + self.name
        print "FDA ID: " + self.id
        print "Vendor: " + self.vendor
        if self.source == "VA":
            print "NOTE: THIS DRUG INFORMATION IS FROM THE VETERANS' AFFAIRS CONTRACT.\nTHESE ARE NOT RETAIL PRICES."
        print "Current Price: $%.2f" % float(self.current[1])
        if self.change > 0:
            print "Lowest Price: $%.2f" % float(self.lowest[1])
        else:
            print "Highest Price: $%.2f" % float(self.highest[1])
        print "Change by percent: %.2f%%" % (self.change * 100)
        # pprint(self.prices)


def builder(csvtext): #csvtext is a str filename
    date = csvtext[-8:]
    drug_dict = {}
    count = 1
    headers = ["Name","FDA ID","Price","Effective date","Pricing Unit","Pharmacy Type","OTC or Not","Explanation Code","Brand or Generic"]
    with open(csvtext+".csv", "r") as drugcsv:
        drugreader = csv.reader(drugcsv)
        for line in drugreader:
            if count < 5:
                pass
            else:
                drug = {}
                for i in range(len(headers)):
                    drug[headers[i]] = line[i]
                price = drug["Price"]
                this_drug = Drug(drug["Name"], drug["FDA ID"], drug["Pricing Unit"],
                                    drug["OTC or Not"], drug["Brand or Generic"], "NADAC")
                Drug.add_price(this_drug, date, price)
                drug_dict[drug["FDA ID"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def consult_va(csvtext, drug_dict):
    count = 1
    date = csvtext[-8:]
    headers = ["Contract Number","Vendor","Start Date","Stop Date","FDA ID","SubItemIdentifier","PackageDesc",
               "Generic Name","TradeName","VAClass","Covered", "Prime Vendor","Price","PriceStart","PriceType"]
    with open(csvtext+".csv", "r") as drugcsv:
        drugreader = csv.reader(drugcsv)
        for line in drugreader:
            if count == 1:
                pass
            else:
                drug = {}
                for i in range(len(headers)):
                    if headers[i] == "FDA ID":
                        drug["FDA ID"] = line[i].translate(None,"-")
                    else:
                        drug[headers[i]] = line[i]
                if drug["FDA ID"] in drug_dict:
                    Drug.add_vendor(drug_dict[drug["FDA ID"]], drug["Vendor"])
                else:
                    this_drug = Drug(drug["TradeName"], drug["FDA ID"], drug["PackageDesc"],
                                     "(Not listed)", "(Not Listed)", "VA")
                    Drug.add_price(this_drug, date, drug["Price"])
                    drug_dict[drug["FDA ID"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def update(csvtext, drug_dict):
    date = csvtext[-8:]
    count = 1
    headers = ["Name","FDA ID","Price","Effective date","Pricing Unit","Pharmacy Type","OTC or Not","Explanation Code","Brand or Generic"]
    with open(csvtext+".csv", "r") as drugcsv:
        drugreader = csv.reader(drugcsv)
        for line in drugreader:
            if count < 5:
                pass
            else:
                drug = {}
                for i in range(len(headers)):
                    drug[headers[i]] = line[i]
                price = drug["Price"]
                if drug["FDA ID"] in drug_dict:
                    Drug.add_price(drug_dict[drug["FDA ID"]], date, price)
                else:
                    this_drug = Drug(drug["Name"], drug["FDA ID"], drug["Pricing Unit"],
                                     drug["OTC or Not"], drug["Brand or Generic"], "NADAC")
                    Drug.add_price(this_drug, date, price)
                    drug_dict[drug["FDA ID"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def return_highest(drug_dict, min_percent, min_price, max_percent, max_price):
    highest = []
    for drug in drug_dict:
        if (min_percent <= drug_dict[drug].change <= max_percent and
            min_price <= drug_dict[drug].current[1] <= max_price):
            highest.append(drug_dict[drug])
        else:
            pass
    return highest


def return_match(drug_dict, search_term):
    matches = []
    for drug in drug_dict:
        if search_term.upper() in (drug_dict[drug].name).upper() and drug_dict[drug].change != 0:
            matches.append(drug_dict[drug])
        else:
            pass
    return matches
	
	
def search_by_str(search):
    sept2015 = "NADAC 20150930"
    nov2013 = "NADAC 20131128"
    va_text = "fssPharmPrices20151001"
    drugs = builder(nov2013)
    drugs = update(sept2015, drugs)
    drugs = consult_va(va_text, drugs)
    drugs = return_match(drugs, search)
    for drug in drugs:
        Drug.printer(drug)
        print
    print "%i RESULTS FOUND" % len(drugs)


def search_by_num(min_percent, min_price, max_percent, max_price):
    sept2015 = "NADAC 20150930"
    nov2013 = "NADAC 20131128"
    va_text = "fssPharmPrices20151001"
    drugs = builder(nov2013)
    drugs = update(sept2015, drugs)
    drugs = consult_va(va_text, drugs)
    drugs = return_highest(drugs, min_percent, min_price, max_percent, max_price)
    for drug in drugs:
        Drug.printer(drug)
        print
    print "%i RESULTS FOUND" % len(drugs)


def remove_stuff(str):
    numstr = ""
    for character in str:
        if character.isdigit() or character == "." or character == "-":
            numstr += character
        else:
            pass
    return numstr


def test():
    search_by_num(1,50,100000,1000000)


if __name__ == "__main__":
    # test()
    print "Let's look at some drug prices."
    print "There are ~22,000 drugs in Medicaid's database, so we need to narrow it down."
    keep_going = "y"
    while keep_going == "y":
        choice = raw_input("Search by (1) drug name or (2) min/max price/%% change. ")
        if choice == "1":
            search = raw_input("Enter your search term: ")
            search_by_str(search)
        elif choice == "2":
            print "Enter minimum and maximum current price and percent increase in two years."
            print "You can just hit enter if you don't want a minimum or maximum."
            raw_min_price = raw_input("MINIMUM CURRENT PRICE: ")
            raw_min_percent = raw_input("MINIMUM PERCENT INCREASE: ")
            raw_max_price = raw_input("MAXIMUM CURRENT PRICE: ")
            raw_max_percent = raw_input("MAXIMUM PERCENT INCREASE: ")
            print
            if raw_min_percent:
                min_percent = float(remove_stuff(raw_min_percent)) / 100
            else:
                min_percent = -10000000
            if raw_min_price:
                min_price = float(remove_stuff(raw_min_price))
            else:
                min_price = 0
            if raw_max_percent:
                max_percent = float(remove_stuff(raw_max_percent)) / 100
            else:
                max_percent = 1000000
            if raw_max_price:
                max_price = float(remove_stuff(raw_max_price))
            else:
                max_price = 100000000
            search_by_num(min_percent, min_price, max_percent, max_price)
        print
        keep_going = (raw_input("RUN ANOTHER SEARCH? Y/N ")).lower()
        print