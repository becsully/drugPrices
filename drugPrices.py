from __future__ import division
import csv
import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.font_manager import FontProperties


class Drug(object):

    """



    """


    def __init__(self, name, ndc, unit, otc, b_or_g, source):
        self.name = name
        self.scientific_name = "(none listed)"
        self.id = ndc
        self.prices = {} #dictionary of datestr: pricefloat
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
        self.desc = ""

    def add_price(self, datestr, price): #datestr formatted YYYYMMDD, price formatted as str
        if price is None:
            self.prices[datestr] = None
        elif datestr in self.prices:
            pass
        else:
            self.prices[datestr] = float(price)
            Drug.update_prices(self)

    def add_vendor(self, vendor):
        self.vendor = vendor

    def add_sci_name(self, name):
        self.scientific_name = name

    def add_desc(self, desc):
        self.desc = desc

    def add_package(self, package):
        self.package = package

    def update_prices(self):
        for date in self.prices:
            if self.prices[date] is None:
                pass
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
        except (ZeroDivisionError, TypeError):
            pass

    def printer(self):
        print "Proprietary name: " + self.name
        print "Scientific name: " + self.scientific_name
        print "NDC: " + self.id
        print "What it is: " + self.desc
        print "Manufacturer: " + self.vendor
        if self.source == "VA":
            print "NOTE: THIS DRUG INFORMATION IS FROM THE VETERANS' AFFAIRS CONTRACT.\nTHESE ARE NOT RETAIL PRICES."
        print "B/G:",
        if self.b_or_g == "B":
            print "Brand"
        elif self.b_or_g == "G":
            print "Generic"
        else:
            print self.b_or_g
        print "Current Price: $%.2f" % float(self.current[1])
        if self.change > 0:
            print "Lowest Price: $%.2f" % float(self.lowest[1])
        else:
            print "Highest Price: $%.2f" % float(self.highest[1])
        print "Change by percent: %.2f%%" % (self.change * 100)
        #print "Prices: ",
        #pprint(self.prices)


def builder(csvtext): #csvtext is a str filename
    date = csvtext[-8:]
    drug_dict = {}
    count = 1
    headers = ["Name","NDC","Price","Effective date","Pricing Unit","Pharmacy Type","OTC or Not","Explanation Code","Brand or Generic"]
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
                this_drug = Drug(drug["Name"], drug["NDC"], drug["Pricing Unit"],
                                    drug["OTC or Not"], drug["Brand or Generic"], "NADAC")
                Drug.add_price(this_drug, date, price)
                drug_dict[drug["NDC"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def multiple_results(drugFDA, choices_list):    # FOR TESTING
                                                # sometimes the simple "if 8-digit-NDC in 11-digit-NDC" search
                                                # returns more than one result. this function prints out the results.
                                                # drugFDA is the dict with FDA info
                                                # choices_list is a list of Drug objects that potentially match
    findings = []
    nameFDA = (drugFDA["PROPRIETARYNAME"].split(" "))[0]
    for choice in choices_list:
        if nameFDA.lower() in (choice.name).lower():
            findings.append(choice)
    return findings


def add_FDA_info(drug_dict):     # this function supplies drug and vendor names via NDCs from the FDA's official database

    name_file = "FDANDCs.csv"
    headers = ["PRODUCTID", "PRODUCTNDC", "PRODUCTTYPENAME", "PROPRIETARYNAME", "PROPRIETARYNAMESUFFIX",
               "NONPROPRIETARYNAME", "DOSAGEFORMNAME", "ROUTENAME", "STARTMARKETINGDATE", "ENDMARKETINGDATE",
               "MARKETINGCATEGORYNAME", "APPLICATIONNUMBER", "LABELERNAME", "SUBSTANCENAME",
               "ACTIVE_NUMERATOR_STRENGTH", "ACTIVE_INGRED_UNIT", "PHARM_CLASSES", "DEASCHEDULE"]
    count = 1
    results = {}
    with open(name_file, "r") as namecsv:
        csvreader = csv.reader(namecsv)
        for line in csvreader:
            if count == 1:
                pass
            else:
                drug = {}
                for i in range(len(headers)):
                    if headers [i] == "PRODUCTNDC":
                        drug["NDC"] = line[i].translate(None,"-")
                        templist = line[i].split("-")
                        templist[0] = templist[0] + "0"
                        drug["NDC2"] = "".join(templist)
                    else:
                        drug[headers[i]] = line[i]
                # print "Looking for NDC " + drug["NDC"] + "..."
                findings = [value for key, value in drug_dict.items() if ( drug["NDC"] in key ) or ( drug["NDC2"] in key )]
                if len(findings) == 1:
                    this_drug = findings[0]
                    Drug.add_vendor(this_drug, drug["LABELERNAME"])
                    Drug.add_sci_name(this_drug, drug["NONPROPRIETARYNAME"])
                    Drug.add_desc(this_drug, drug["PHARM_CLASSES"])
                elif len(findings) == 0:
                    pass
                else:
                    findings = multiple_results(drug, findings)
                    for finding in findings:
                        Drug.add_vendor(finding, drug["LABELERNAME"])
                        Drug.add_sci_name(finding, drug["NONPROPRIETARYNAME"])
                        Drug.add_desc(finding, drug["PHARM_CLASSES"])

                            # BECAUSE THE FDA NDCS ARE ONLY EIGHT DIGITS LONG, THIS SEARCH OFTEN RETURNS 2+ RESULTS.
                            # TODO: write a function to check other info to figure out which is the correct one.
                            # or, worst-case scenario, prompt user to choose which looks right, maybe?
                #for finding in findings:
                #    results[drug["NDC"]] = finding
            count += 1
    """print str(len(results)) + " results found...."
    print
    for result in sorted(results):
        print "Search ID " + result
        Drug.printer(results[result])
        print"""
    return drug_dict


def consult_va(csvtext, drug_dict):
    count = 1
    date = csvtext[-8:]
    headers = ["Contract Number","Vendor","Start Date","Stop Date","NDC","SubItemIdentifier","PackageDesc",
               "Generic Name","TradeName","VAClass","Covered", "Prime Vendor","Price","PriceStart","PriceType"]
    with open(csvtext+".csv", "r") as drugcsv:
        drugreader = csv.reader(drugcsv)
        for line in drugreader:
            if count == 1:
                pass
            else:
                drug = {}
                for i in range(len(headers)):
                    if headers[i] == "NDC":
                        drug["NDC"] = line[i].translate(None,"-")
                    else:
                        drug[headers[i]] = line[i]
                if drug["NDC"] in drug_dict:
                    Drug.add_vendor(drug_dict[drug["NDC"]], drug["Vendor"])
                else:
                    this_drug = Drug(drug["TradeName"], drug["NDC"], drug["PackageDesc"],
                                     "(Not listed)", "(Not Listed)", "VA")
                    Drug.add_price(this_drug, date, drug["Price"])
                    drug_dict[drug["NDC"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def update(csvtext, drug_dict):
    date = csvtext[-8:]
    count = 1
    headers = ["Name","NDC", "Price", "Effective date", "Pricing Unit", "Pharmacy Type",
               "OTC or Not", "Explanation Code", "Brand or Generic"]
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
                if drug["NDC"] in drug_dict:
                    Drug.add_price(drug_dict[drug["NDC"]], date, price)
                else:
                    this_drug = Drug(drug["Name"], drug["NDC"], drug["Pricing Unit"],
                                     drug["OTC or Not"], drug["Brand or Generic"], "NADAC")
                    Drug.add_price(this_drug, date, price)
                    drug_dict[drug["NDC"]] = this_drug
            count += 1
        drugcsv.close()
    return drug_dict


def add_prices(csvtext, drug_dict):
    date = csvtext[-8:]
    count = 1
    headers = ["Name","NDC", "Price", "Effective date", "Pricing Unit", "Pharmacy Type",
               "OTC or Not", "Explanation Code", "Brand or Generic"]
    drug_list = [drug for drug in drug_dict]
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
                if drug["NDC"] in drug_dict:
                    Drug.add_price(drug_dict[drug["NDC"]], date, price)
                    drug_list.remove(drug["NDC"])
                else:
                    pass
            count += 1
        drugcsv.close()
    for drug in drug_list:
        Drug.add_price(drug_dict[drug], date, None)
    return drug_dict


def return_highest(drug_dict, min_percent, min_price, max_percent, max_price):
    highest = {}
    for drug in drug_dict:
        if (min_percent <= drug_dict[drug].change <= max_percent and
            min_price <= drug_dict[drug].current[1] <= max_price):
            highest[drug] = drug_dict[drug]
        else:
            pass
    return highest


def return_match(drug_dict, search_term):
    matches = {}
    for drug in drug_dict:
        if ( ( search_term.upper() in (drug_dict[drug].name).upper())
             or ( search_term.upper() in (drug_dict[drug].scientific_name).upper())) and (drug_dict[drug].prices > 1):
            matches[drug] = drug_dict[drug]
        else:
            pass
    return matches


def start():
    latest = "nadac/NADAC 20151111"
    middle = "nadac/NADAC 20141119"
    earliest = "nadac/NADAC 20131128"
    #va_text = "fssPharmPrices20151001"
    drugs = builder(earliest)
    drugs = update(middle, drugs)
    drugs = update(latest, drugs)
    return drugs


def get_date_list():
    return ["20131128","20131204","20131211","20131218","20131225","20140101","20140108","20140115","20140122","20140129",
            "20140205","20140212","20140219","20140226","20140305","20140312","20140319","20140326","20140402",
            "20140409","20140416","20140423","20140430","20140507","20140514","20140521","20140528","20140604",
            "20140611","20140618","20140625","20140702","20140709","20140716","20140723","20140730","20140806",
            "20140813","20140820","20140827","20140903","20140910","20140917","20140924","20141001","20141008",
            "20141015","20141022","20141029","20141105","20141112","20141119","20141126","20141203","20141210",
            "20141217","20141224","20141231","20150107","20150114","20150121","20150128","20150204","20150211",
            "20150218","20150225","20150304","20150311","20150318","20150325","20150401","20150415","20150422",
            "20150429","20150506","20150513","20150520","20150527","20150603","20150610","20150617","20150624",
            "20150701","20150708","20150715","20150722","20150729","20150805","20150812","20150819","20150826",
            "20150902","20150909","20150916","20150923","20150930","20151007","20151014","20151021","20151028",
            "20151104","20151111"]


def fill_in(drugs):
    date_list = get_date_list()
    for date in date_list:
        print ".",
        drugs = add_prices("nadac/NADAC " + date, drugs)
    print
    return drugs


def draw_graph(drug_dict):
    colors = [(114/255, 158/255, 206/255), (255/255, 158/255, 74/255), (103/255, 191/255, 92/255),
              (237/255, 102/255, 93/255), (173/255, 139/255, 201/255), (168/255, 120/255, 110/255),
              (237/255, 151/255, 202/255), (162/255, 162/255, 162/255), (205/255, 204/255, 93/255),
              (109/255, 204/255, 218/255)]
    xlist = get_date_list()
    x = []
    for date in xlist:
        date = datetime.datetime.strptime(date,"%Y%m%d")
        x.append(date)
    y_dict = {}
    for drug in drug_dict:
        drug_name = drug_dict[drug].name
        y_dict[drug_name] = []
        for k in sorted(drug_dict[drug].prices):
            y_dict[drug_name].append(drug_dict[drug].prices[k])
            #if date not in x:
            #    x.append(date)
    #print x
    #print y
    dates = mdates.date2num(x)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    count = 0
    for y in y_dict:
        graph.plot(dates, y_dict[y], lw=2.5, color=colors[count], label=y)
        first = None
        for price in y_dict[y]:
            first = price
            if first is not None:
                break
        plt.annotate('$%0.2f' % first, xy=(0.1, first), xytext=(0, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points', color=colors[count])
        plt.annotate('$%0.2f' % y_dict[y][-1], xy=(.9, y_dict[y][-1]), xytext=(1, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points', color=colors[count])
        count += 1
    leg = graph.legend(loc=2)
    conv = np.vectorize(mdates.strpdate2num('%Y%m%d'))
    graph.axvline(conv('20140101'), color='lightgrey', zorder=0)
    graph.axvline(conv('20150101'), color='lightgrey', zorder=0)
    graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    graph.xaxis.set_major_locator(mdates.MonthLocator())
    graph.xaxis.set_minor_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

    fig.autofmt_xdate()

    for color, text in zip(colors,leg.get_texts()):
        text.set_color(color)

    plt.show()


def ask_for_graph(drug_dict):
    choice = raw_input("Print a graph? Type the number of the result, or just hit enter to pass. ")
    while choice:
        chosen_drugs = {}
        count = 0
        choices = choice.split(",")
        int_choices = []
        for choice in choices:
            int_choices.append(int(choice.replace(" ", "")))
        for drug in drug_dict:
            count += 1
            if count in int_choices:
                chosen_drugs[drug] = drug_dict[drug]
        fill_in(chosen_drugs)
        draw_graph(chosen_drugs)
        choice = raw_input("PRINT A GRAPH? Type the result number (or numbers, separated by comma), or hit enter to skip. ")


def search_by_str():
    search = raw_input("Enter your search term: ")
    drugs = start()
    drugs = return_match(drugs, search)
    if len(drugs) > 0:
        drugs = add_FDA_info(drugs)
        count = 1
        for drug in drugs:
            print str(count) + "."
            Drug.printer(drugs[drug])
            print
            count += 1
        ask_for_graph(drugs)
    else:
        print "No results."


def search_by_num():  #
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
    drugs = start()
    drugs = return_highest(drugs, min_percent, min_price, max_percent, max_price)
    if len(drugs) > 0:
        drugs = add_FDA_info(drugs)
        count = 1
        print
        for drug in drugs:
            print str(count) + "."
            Drug.printer(drugs[drug])
            print
            count += 1
        ask_for_graph(drugs)
    else:
        print "No results."


def remove_stuff(str):  # removes non-number characters from the main() raw_inputs
    numstr = ""
    for character in str:
        if character.isdigit() or character == "." or character == "-":
            numstr += character
        else:
            pass
    return numstr


def test():
    drugs = start()


if __name__ == "__main__":
    print "Let's look at some drug prices."
    print "There are ~24,000 drugs in Medicaid's database, so we need to narrow it down."
    keep_going = "y"
    while keep_going == "y":
        choice = raw_input("Search by (1) drug name or (2) min/max price/%% change. ")
        if choice == "1":
            search_by_str()
        elif choice == "2":
            search_by_num()
        elif choice == "test":
            test()
        else:
            print "Pick 1 or 2."
        print
        keep_going = (raw_input("RUN ANOTHER SEARCH? Y/N ")).lower()
        print