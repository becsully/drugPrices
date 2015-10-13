# drugPrices
a script to compare prescription drug prices

Prescription drugs are getting more expensive at a rate much faster than inflation. 
This script looks at pricing data from the Centers of Medicare and Medicaid Services and
shows how those prices have changed from 2013 to today. 

It's a work in progress, but the basic searches run on any computer with basic Python 2.7. 
(The only module needed to run the basic search is csv, which is included in Python 2.3+.)

Download the repo and run drugPrices.py to search by a drug's name, or to find all drugs whose
prices and price changes fall within your given minimums and maximums. 

Sample output: 

```
Let's look at some drug prices.
There are ~22,000 drugs in Medicaid's database, so we need to narrow it down.
Search by (1) drug name or (2) min/max price/%% change. 2
Enter minimum and maximum current price and percent increase in two years.
You can just hit enter if you don't want a minimum or maximum.
MINIMUM CURRENT PRICE: $50
MINIMUM PERCENT INCREASE: 500%
MAXIMUM CURRENT PRICE: 
MAXIMUM PERCENT INCREASE: 

Proprietary name: TASMAR 100 MG TABLET
Scientific name: Tolcapone
NDC: 00187093801
What it is: Catechol O-Methyltransferase Inhibitors [MoA],Catechol-O-Methyltransferase Inhibitor [EPC]
Manufacturer: Valeant Pharmaceuticals North America LLC
B/G: Brand
Current Price: $105.98
Lowest Price: $15.70
Change by percent: 575.00%

Proprietary name: CARAC CREAM
Scientific name: fluorouracil
NDC: 00066715030
What it is: Nucleic Acid Synthesis Inhibitors [MoA],Nucleoside Metabolic Inhibitor [EPC]
Manufacturer: Dermik Laboratories
B/G: Brand
Current Price: $81.53
Lowest Price: $13.33
Change by percent: 511.48%

2 RESULTS FOUND

RUN ANOTHER SEARCH? Y/N 
```
