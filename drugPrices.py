from __future__ import division
import csv
import time
from pprint import pprint


class Drug(object):
    def __init__(self, name, fda_id, unit, otc, b_or_g):
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

    def add_price(self, datestr, price): #date str formatted YYYYMMDD, float
        self.prices[datestr] = float(price)
        Drug.update_prices(self)

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
        self.change = ( self.current[1] / self.oldest[1] ) - 1

    def printer(self):
        print "Name: " + self.name
        print "FDA ID: " + self.id
        print "Current Price: $%.2f" % float(self.current[1])
        print "Lowest Price: $%.2f" % float(self.lowest[1])
        print "Change by percent: %.2f%%" % (self.change * 100)
        pprint(self.prices)


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
                                    drug["OTC or Not"], drug["Brand or Generic"])
                Drug.add_price(this_drug, date, price)
                drug_dict[drug["FDA ID"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def create_new(drug_dict):
    # TODO potentially -- write a separate function outside of builder() to reuse as much as possible
    pass


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
                                     drug["OTC or Not"], drug["Brand or Generic"])
                    Drug.add_price(this_drug, date, price)
                    drug_dict[drug["FDA ID"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def return_highest(drug_dict, percent, price):
    highest = []
    for drug in drug_dict:
        if drug_dict[drug].change > percent and drug_dict[drug].highest[1] > price:
            highest.append(drug_dict[drug])
        else:
            pass
    return highest


def here_we_go(percent, price):
    test1 = "NADAC 20150930"
    test2 = "NADAC 20131128"
    drugs = builder(test1)
    drugs = update(test2, drugs)
    drugs = return_highest(drugs, percent, price)
    for drug in drugs:
        Drug.printer(drug)
        print


def remove_stuff(str):
    numstr = ""
    for character in str:
        if character.isdigit():
            numstr += character
        else:
            pass
    return numstr


if __name__ == "__main__":
    print "Let's look at some drug prices."
    print "There are ~22,000 drugs in Medicaid's database, so we need to narrow it down."
    print "Enter a minimum percent increase you'd like to see, and a minimum current price."
    raw_percent = raw_input("MINIMUM PERCENT INCREASE: ")
    raw_price = raw_input("MINIMUM CURRENT PRICE: ")
    print
    percent = int(remove_stuff(raw_percent)) / 100
    price = int(remove_stuff(raw_price))
    here_we_go(percent, price)
