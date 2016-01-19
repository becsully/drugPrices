from __future__ import division
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests
from glob import glob
import zipfile
import StringIO
import xlrd
import shutil
import os
from drug import Drug, return_highest, return_match, start, builder, add_FDA_info, add_prices, update, get_date_list, \
    fill_in, remove_stuff


def get_file():
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.makedirs('temp')
    base_url = "http://www.medicaid.gov/Medicaid-CHIP-Program-Information/By-Topics/Benefits/Prescription-Drugs/Downloads/NADAC/"
    base_end = "-NADAC-Files.zip"
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%B")
    full_url = base_url + date_str + base_end
    r = requests.get(full_url)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall("temp")


def convert_to_csv():
    for path in glob("temp/*.xl*"):
        filename = os.path.basename(path).split(".")[0]
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        output = open("nadac/%s.csv" % filename, "wb")
        writer = csv.writer(output)
        for rownum in xrange(sheet.nrows):
            writer.writerow(sheet.row_values(rownum))
        output.close()


def get_first_last(price_list):
    # this function returns the first and last date with a non-None price
    # this allows the draw_graph() function to add price info at the beginning and end of the lines
    for price in price_list:
        first = price
        if first is not None:
            break
    for price in reversed(price_list):
        last = price
        if last is not None:
            break
    return first, last


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

    dates = mdates.date2num(x)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    count = 0
    for y in y_dict:
        graph.plot(dates, y_dict[y], lw=2.5, color=colors[count], label=y)
        first, last = get_first_last(y_dict[y])
        plt.annotate('$%0.2f' % first, xy=(0.1, first), xytext=(0, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points', color=colors[count])
        plt.annotate('$%0.2f' % last, xy=(.9, last), xytext=(1, 0),
             xycoords=('axes fraction', 'data'), textcoords='offset points', color=colors[count])
        count += 1
    leg = graph.legend(loc=2)
    conv = np.vectorize(mdates.strpdate2num('%Y%m%d'))
    graph.axvline(conv('20140101'), color='lightgrey', zorder=0)
    graph.axvline(conv('20150101'), color='lightgrey', zorder=0)
    graph.axvline(conv('20160101'), color='lightgrey', zorder=0)
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


def search_by_num():
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


def test():
    get_file()
    convert_to_csv()


def menu():
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


if __name__ == "__main__":
    menu()