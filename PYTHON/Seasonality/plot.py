import matplotlib.pylab as plt, os, pandas as pd,  numpy as np, seaborn as sns

database = pd.read_csv(os.getcwd()+"/Seasonality_Data.txt",sep="\t")

plt.title("LAM Portfolio - Seasonality")
plt.ylabel("Return on Initial AUM of $1m")
plt.bar(range(len(database["Month"])),database["Percentage"], color='k')
plt.xticks(range(len(database["Month"])), ["JAN", "FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"])
plt.savefig(os.getcwd()+"/LAM_Portfolio_Seasonality.png", dpi=300)