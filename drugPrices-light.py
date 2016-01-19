from __future__ import division
import csv
import datetime
from drug import Drug, builder, add_FDA_info, multiple_results, update, add_prices, return_highest, return_match, start, remove_stuff


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
    else:
        print "No results."


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