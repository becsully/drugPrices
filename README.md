# drugPrices

Prescription drugs are getting more expensive. And it's happening much, much faster than inflation. 

This script looks at the prices that pharmacies pay to acquire the drugs that we buy -- and it shows how those prices have changed, week by week, from 2013 to today. (The data comes from the Centers for Medicare and Medicaid Services, which survey hundreds of pharmacies every week about how much they pay for drugs.)

This repo contains a pair of similar scripts whichallow you to search by a drug's name, or to find all drugs whose prices and price changes (by percent) fall within your given parameters. 

Download the repo and run **drugPrices-light.py** to receive text results only. The light version needs only Python 2.7 to run. 

To graph your results, run **drugPrices-graphy.py**. You'll need *numpy* and *matplotlib*. The graphs aren't pretty yet, but they're a useful visual tool to help spot patterns and important dates. 

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
