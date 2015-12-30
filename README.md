# drugPrices

Prescription drugs are getting more expensive. And it's happening much, much faster than inflation. This script looks at the average prices that pharmacies are paying to acquire the drugs we buy, and shows how those prices have changed from 2013 to today. (The data comes from the Centers for Medicare and Medicaid Services, which survey hundreds of pharmacies each week about how much they are paying for drugs.)

Right now, the script requires Python 2.7 and two common modules that are not included in a basic Python install: *numpy* and *matplotlib*. Installing via Anaconda will include them. 

(I plan to add a basic version of the search, which will run on any computer with Python 2.3+.)

Download the repo and run drugPrices.py to search by a drug's name, or to find all drugs whose prices and price changes (by percent) fall within your given parameters. 

Sample output: 

```
Let's look at some drug prices.
There are ~22,000 drugs in Medicaid's database, so we need to narrow it down.
Search by (1) drug name or (2) min/max price/% change. 2
Enter minimum and maximum current price and percent increase in two years.
You can just hit enter if you don't want a minimum or maximum.
MINIMUM CURRENT PRICE: $50
MINIMUM PERCENT INCREASE: 500%
MAXIMUM CURRENT PRICE: 
MAXIMUM PERCENT INCREASE: 

1.
Proprietary name: TASMAR 100 MG TABLET
Scientific name: Tolcapone
NDC: 00187093801
What it is: Catechol O-Methyltransferase Inhibitors [MoA],Catechol-O-Methyltransferase Inhibitor [EPC]
Manufacturer: Valeant Pharmaceuticals North America LLC
B/G: Brand
Current Price: $105.98
Lowest Price: $15.70
Change by percent: 575.00%

2.
Proprietary name: CARAC CREAM
Scientific name: fluorouracil
NDC: 00066715030
What it is: Nucleic Acid Synthesis Inhibitors [MoA],Nucleoside Metabolic Inhibitor [EPC]
Manufacturer: Dermik Laboratories
B/G: Brand
Current Price: $81.53
Lowest Price: $13.33
Change by percent: 511.48%

Print a graph? Type the number of the result, or just hit enter to pass. 

RUN ANOTHER SEARCH? Y/N n
```
