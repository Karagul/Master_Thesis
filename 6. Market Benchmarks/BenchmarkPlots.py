import matplotlib.pylab as plt, os, pandas as pd,  numpy as np, seaborn as sns
import numpy as np
import matplotlib.mlab as mlab


database = pd.read_csv(os.getcwd()+"/Source.txt", sep="\t")

LMA_Portfolio_Equity = []
BARCCURR_Equity = []
BARCSYST_Equity = []
BARCBTOP_Equity = []
MSCI_World_Equity = []

for i in range(0,len(database)):
	if (i==0):
		LMA_Portfolio_Equity.append(database["LMA Portfolio"][i]*100+100)
		BARCCURR_Equity.append(database["BARCCURR"][i]*100+100)
		BARCSYST_Equity.append(database["BARCSYST"][i]*100+100)
		BARCBTOP_Equity.append(database["BARCBTOP"][i]*100+100)
		MSCI_World_Equity.append(database["MSCI World"][i]*100+100)
	else:
		LMA_Portfolio_Equity.append(database["LMA Portfolio"][i]*LMA_Portfolio_Equity[-1]+LMA_Portfolio_Equity[-1])
		BARCCURR_Equity.append(database["BARCCURR"][i]*BARCCURR_Equity[-1]+BARCCURR_Equity[-1])
		BARCSYST_Equity.append(database["BARCSYST"][i]*BARCSYST_Equity[-1]+BARCSYST_Equity[-1])
		BARCBTOP_Equity.append(database["BARCBTOP"][i]*BARCBTOP_Equity[-1]+BARCBTOP_Equity[-1])
		MSCI_World_Equity.append(database["MSCI World"][i]*MSCI_World_Equity[-1]+MSCI_World_Equity[-1])

plt.figure(1).clf()
plt.title("LAM Portfolio vs. Market Benchmarks - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.07.2007 to 31.12.2016 [months]")
plt.ylabel("Index")
plt.plot(LMA_Portfolio_Equity,color='k',label="LAM Portfolio")
plt.plot(BARCCURR_Equity,color='b',label="BARCCURR")
plt.plot(BARCSYST_Equity,color='g',label="BARCSYST")
plt.plot(BARCBTOP_Equity,color='r',label="BARCBTOP")
plt.plot(MSCI_World_Equity,color='y',label="MSCI World")
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/LAM_vs_MarketBenchmarks.png", dpi=300)


plt.figure(2).clf()
plt.title("BARCCURR - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(database["BARCCURR"], bins=20, color='k')
plt.hist(database["LMA Portfolio"],bins=20, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/BARCCURR_Returns_Distribution.png", dpi=300)

plt.figure(3).clf()
plt.title("BARCSYST - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(database["BARCSYST"], bins=20, color='k')
plt.hist(database["LMA Portfolio"],bins=20, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/BARCSYST_Returns_Distribution.png", dpi=300)

plt.figure(4).clf()
plt.title("BARCBTOP - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(database["BARCBTOP"], bins=20, color='k')
plt.hist(database["LMA Portfolio"],bins=20, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/BARCBTOP_Returns_Distribution.png", dpi=300)

plt.figure(5).clf()
plt.title("MSCI World - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(database["MSCI World"], bins=20, color='k')
plt.hist(database["LMA Portfolio"],bins=20, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/MSCI_World_Returns_Distribution.png", dpi=300)

plt.figure(6).clf()
plt.title("LAM Portfolio - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(database["LMA Portfolio"], bins=20, color='k')
plt.savefig(os.getcwd()+"/LAM_Portfolio_Returns_Distribution.png", dpi=300)


plt.figure(7).clf()
plt.title("LAM Portfolio vs. Model Benchmarks - Correlations (12 months rolling)")
plt.ylabel("Correlation")
plt.xlabel("Time Period 01.07.2008 to 31.12.2016 [months]")
plt.plot(pd.rolling_corr(database['LMA Portfolio'],database['BARCCURR'],window=12),color='b',linewidth=1.0,label="BARCCURR")
plt.plot(pd.rolling_corr(database['LMA Portfolio'],database['BARCSYST'],window=12),color='g',linewidth=1.0,label="BARCSYST")
plt.plot(pd.rolling_corr(database['LMA Portfolio'],database['BARCBTOP'],window=12),color='r',linewidth=1.0,label="BARCBTOP")
plt.plot(pd.rolling_corr(database['LMA Portfolio'],database['MSCI World'],window=12),color='y',linewidth=1.0,label="MSCI World")
plt.legend(loc='upper right', prop={'size':8})
plt.savefig(os.getcwd()+"/Correlations.png", dpi=300)

