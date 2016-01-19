import csv
from drug import Drug, get_date_list, builder, update, multiple_results


def new_fda(drug_dict):

    # this function supplies drug and vendor names via NDCs from the FDA's official database.
    # sadly the FDA and NADAC have a slightly different format for NDCs, so it's not perfect.
    # It is very unlikely to assign an incorrect NDC -- rather, it will pass on drugs it cannot find a match for.

    name_file = "FDA-20160118.csv"
    headers = ["PRODUCTID", "PRODUCTNDC", "PRODUCTTYPENAME", "PROPRIETARYNAME", "PROPRIETARYNAMESUFFIX",
               "NONPROPRIETARYNAME", "DOSAGEFORMNAME", "ROUTENAME", "STARTMARKETINGDATE", "ENDMARKETINGDATE",
               "MARKETINGCATEGORYNAME", "APPLICATIONNUMBER", "LABELERNAME", "SUBSTANCENAME",
               "ACTIVE_NUMERATOR_STRENGTH", "ACTIVE_INGRED_UNIT", "PHARM_CLASSES", "DEASCHEDULE"]
    count = 1
    results = {}
    current_list = [key for key in drug_dict]
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
                findings = [item for item in current_list if ( drug["NDC"] in item ) or ( drug["NDC2"] in item )]
                if len(findings) == 1:
                    this_drug = drug_dict[findings[0]]
                    Drug.add_vendor(this_drug, drug["LABELERNAME"])
                    Drug.add_sci_name(this_drug, drug["NONPROPRIETARYNAME"])
                    Drug.add_desc(this_drug, drug["PHARM_CLASSES"])
                    current_list.remove(findings[0])
                    print "%i drugs left to ID..." % len(current_list)
                elif len(findings) == 0:
                    pass
                else:
                    findings_as_drugs = [drug_dict[key] for key in findings] #converts list of keys into list of Drugs
                    findings = multiple_results(drug, findings_as_drugs) #list of Drugs
                    for finding in findings: #finding is a Drug
                        Drug.add_vendor(finding, drug["LABELERNAME"])
                        Drug.add_sci_name(finding, drug["NONPROPRIETARYNAME"])
                        Drug.add_desc(finding, drug["PHARM_CLASSES"])
                        current_list.remove(finding.id)
                        print "%i drugs left to ID..." % len(current_list)

                            # BECAUSE THE FDA NDCS ARE ONLY EIGHT DIGITS LONG, THIS SEARCH OFTEN RETURNS 2+ RESULTS.
                            # TODO: write a function to check other info to figure out which is the correct one.
                            # or, worst-case scenario, prompt user to choose which looks right, maybe?
            count += 1

    return drug_dict


def create_list():
    raw_dates = get_date_list()
    files = []
    for i in range(len(raw_dates)):
        filename = "nadac/NADAC " + raw_dates[i]
        files.append(filename)
    drugs = builder(files[0])
    for i in range(len(files)-1):
        update(files[i+1], drugs)
        print "done with %s" % files[i+1]
    return new_fda(drugs)


def write(drugs):
    fieldnames = ["ID", "Name", "Scientific Name", "Unit", "OTC", "Brand/Generic", "Vendor", "Package", "Description"]
    dates = get_date_list()
    for i in range(len(dates)):
        fieldnames.append(dates[i])
    with open("FullPrices.csv","a") as prices_csv:
        writer = csv.writer(prices_csv, delimiter='|')
        writer.writerow(fieldnames)
        for entry in drugs:
            drug = drugs[entry]
            drugrow = [drug.id, drug.name, drug.scientific_name, drug.unit, drug.otc, drug.b_or_g, drug.vendor, drug.package, drug.desc]
            for i in range(len(dates)):
                try:
                    drugrow.append(drug.prices[dates[i]])
                except KeyError:
                    drugrow.append(None)
            writer.writerow(drugrow)
        prices_csv.close()
    print "Done"


if __name__ == '__main__':
    drugs = create_list()
    count = 0
    for drug in drugs:
        print "%i." % count
        Drug.printer(drugs[drug])
        print
        count += 1
    write(drugs)