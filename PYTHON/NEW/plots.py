import matplotlib.pylab as plt, os, pandas as pd,  numpy as np, seaborn as sns


database = pd.read_csv(os.getcwd()+"/In_Sample_Optimization_12000.txt")



Returns_LAM = filter(lambda a: a != 0, database["Portfolio"].tolist())
Returns_Bench1 = filter(lambda a: a != 0, database["EW_Portfolio"].tolist())
Returns_Bench2 = filter(lambda a: a != 0, database["BASE_Portfolio"].tolist())

Equity_LAM = []
Equity_Bench1 = []
Equity_Bench2 = []

PL_LAM = []
PL_Bench1 = []
PL_Bench2 = []

for i in range(0,len(Returns_LAM)):
	if (i==0):
		Equity_LAM.append(1000000*(1+2*Returns_LAM[i]))
		PL_LAM.append(Equity_LAM[i]-1000000)
		Equity_Bench1.append(1000000*(1+2*Returns_Bench1[i]))
		Equity_Bench2.append(1000000*(1+2*Returns_Bench2[i]))
	else:
		Equity_LAM.append(Equity_LAM[i-1]*(1+2*Returns_LAM[i]))
		PL_LAM.append(Equity_LAM[i]-Equity_LAM[i-1])
		Equity_Bench1.append(Equity_Bench1[i-1]*(1+2*Returns_Bench1[i]))
		Equity_Bench2.append(Equity_Bench2[i-1]*(1+2*Returns_Bench2[i]))

plt.figure(1).clf()
plt.title("LAM Portfolio - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.07.2007 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot(Equity_LAM, color='k')
plt.axvline(x=48, color='k', linestyle='--')
plt.axvline(x=97, color='k', linestyle='--')
plt.axvline(x=145, color='k', linestyle='--')
plt.axvline(x=193, color='k', linestyle='--')
plt.axvline(x=242, color='k', linestyle='--')
plt.axvline(x=289, color='k', linestyle='--')
plt.axvline(x=337, color='k', linestyle='--')
plt.axvline(x=385, color='k', linestyle='--')
plt.axvline(x=433, color='k', linestyle='--')
plt.savefig(os.getcwd()+"/LAM_Portfolio.png", dpi=300)



plt.figure(2).clf()
plt.title("LAM Portfolio vs. Model Benchmarks - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.07.2007 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot(Equity_LAM, label="LAM Portfolio", color='k')
plt.plot(Equity_Bench1, label="Benchmark 1", linestyle='--', color='b')
plt.plot(Equity_Bench2, label="Benchmark 2", linestyle='--', color='g')
plt.legend(loc='upper left', prop={'size':8})
plt.axvline(x=48, color='k', linestyle='--')
plt.axvline(x=97, color='k', linestyle='--')
plt.axvline(x=145, color='k', linestyle='--')
plt.axvline(x=193, color='k', linestyle='--')
plt.axvline(x=242, color='k', linestyle='--')
plt.axvline(x=289, color='k', linestyle='--')
plt.axvline(x=337, color='k', linestyle='--')
plt.axvline(x=385, color='k', linestyle='--')
plt.axvline(x=433, color='k', linestyle='--')
plt.savefig(os.getcwd()+"/LAM_Portfolio_ModelBenchmarks.png", dpi=300)


plt.figure(3).clf()
plt.title("LAM Portfolio - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(Returns_LAM, bins=40, color='k')
plt.savefig(os.getcwd()+"/LAM_Portfolio_Returns_Distribution.png", dpi=300)

plt.figure(4).clf()
plt.title("Model Benchmark 1 - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(Returns_Bench1, bins=40, color='k')
plt.hist(Returns_LAM,bins=40, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/Benchmark1_Returns_Distribution.png", dpi=300)

plt.figure(5).clf()
plt.title("Model Benchmark 2 - Returns Distribution")
plt.ylabel("Frequency")
plt.xlabel("Returns")
plt.hist(Returns_Bench2, bins=40, color='k')
plt.hist(Returns_LAM,bins=40, histtype = 'step', label="LAM Portfolio",color='y',linewidth=2.0)
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/Benchmark2_Returns_Distribution.png", dpi=300)
