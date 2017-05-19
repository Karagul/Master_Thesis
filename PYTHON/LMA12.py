import os, pandas as pd, random, math, matplotlib.pyplot as plt, decimal, numpy as np
from matplotlib.offsetbox import AnchoredText

def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total

Equity = 1000000
Iterations = 30000
RiskFree = 0
Directory1 = os.getcwd()+"/Output/DE_LM_AM/"
Directory2 = os.getcwd()+"/Output/Comm_NonComm/"


def Random_Weights(n):
	random_weights = []
	for i in xrange(n):
		random_weights.append(random.randint(5, 50) / 100.0)
	return [round(x / sum(random_weights),4) for x in random_weights]


Files1 = os.listdir(Directory1)
Files2 = os.listdir(Directory2)

#Read LMA Database
LMA_DataFrame = pd.read_csv(os.getcwd()+"/LMA_Database.txt")
LMA_DataFrame["Trade_Date"] = pd.to_datetime(LMA_DataFrame["Trade_Date"], format='%d.%m.%Y')

# Import data
for i in range(0,len(Files1)):
	if ".csv" in Files1[i]:
		#Extract Asset
		Asset = Files1[i][:6]
		Participant = Files1[i].split('_')[1]

		Loaded_DataFrame = pd.read_csv(Directory1 + Files1[i])
		Provisionary_DataFrame = Loaded_DataFrame.loc[:,['Trade_Date','Basic_PL','AR_Comb_PL','GARCH_PL']]

		Provisionary_DataFrame["Trade_Date"] = pd.to_datetime(Provisionary_DataFrame["Trade_Date"])
		Provisionary_DataFrame = Provisionary_DataFrame.rename(columns={'Basic_PL': str('BASE_'+Asset+'_'+Participant), 'AR_Comb_PL': str('AR_'+Asset+'_'+Participant), 'GARCH_PL': str('GARCH_'+Asset+'_'+Participant)})

		LMA_DataFrame = pd.merge(LMA_DataFrame, Provisionary_DataFrame, on='Trade_Date', how='inner')
for i in range(0,len(Files2)):
	if ".csv" in Files2[i]:
		#Extract Asset
		Asset = Files2[i][:6]
		Participant = Files2[i].split('_')[1]

		Loaded_DataFrame = pd.read_csv(Directory2 + Files2[i])
		Provisionary_DataFrame = Loaded_DataFrame.loc[:,['Trade_Date','Basic_PL','AR_Comb_PL','GARCH_PL']]

		Provisionary_DataFrame["Trade_Date"] = pd.to_datetime(Provisionary_DataFrame["Trade_Date"])
		Provisionary_DataFrame = Provisionary_DataFrame.rename(columns={'Basic_PL': str('BASE_'+Asset+'_'+Participant), 'AR_Comb_PL': str('AR_'+Asset+'_'+Participant), 'GARCH_PL': str('GARCH_'+Asset+'_'+Participant)})

		LMA_DataFrame = pd.merge(LMA_DataFrame, Provisionary_DataFrame, on='Trade_Date', how='inner')

# Convert to returns
for i in range(1,len(LMA_DataFrame.columns)):
	LMA_DataFrame[LMA_DataFrame.columns[i]] =  pd.DataFrame(map(lambda x:x+Equity, list(accumu(LMA_DataFrame[LMA_DataFrame.columns[i]].tolist())))).pct_change(1)

# Delete First line of the dataframe since it does not contain data
LMA_DataFrame.drop(LMA_DataFrame.index[:1], inplace=True)
LMA_DataFrame = LMA_DataFrame.reset_index(drop=True)
LMA_DataFrame_New = LMA_DataFrame.copy()

def MeanVariance(Iterations,LMA_DataFrame,LookBackFrom,LookBackTo, Mode):
	Strategy_Annualized_Return = []
	Strategy_Annualized_Vola = []
	Strategy_Sharpe_Ratio = []
	Strategy_Composition = []
	Strategy_Weights = []
	for j in range(0,Iterations):

		#Create 10 random weights
		Weights = Random_Weights(5)
		if Mode == "FULL":
			Assets = LMA_DataFrame.sample(n=5, axis=1)[LookBackFrom:LookBackTo]
		else:
			Assets = LMA_DataFrame.ix[:, [c for c in LMA_DataFrame.columns if c.startswith("BASE")]].sample(n=5, axis=1)[LookBackFrom:LookBackTo]

		while ("Trade_Date" in Assets):
			if Mode == "FULL":
				Assets = LMA_DataFrame.sample(n=5, axis=1)[LookBackFrom:LookBackTo]
			else:
				Assets = LMA_DataFrame.ix[:, [c for c in LMA_DataFrame.columns if c.startswith("BASE")]].sample(n=5, axis=1)[LookBackFrom:LookBackTo]

		Adjusted_Database = Weights*Assets
		Adjusted_Database["PortfolioReturns"] = Adjusted_Database.sum(axis=1)
		
		Returns = Adjusted_Database["PortfolioReturns"].mean()*52
		Volatility = Adjusted_Database["PortfolioReturns"].std()*math.sqrt(52)
		Sharpe = (Returns - RiskFree) / Volatility

		assets_string = "";
		for i in range(0,len(Adjusted_Database.columns)):
			assets_string = assets_string + " " + Adjusted_Database.columns[i]

		weights_string = "";
		for i in range(0,len(Weights)):
			weights_string = weights_string + " " + str(Weights[i])
		
		Strategy_Annualized_Return.append(Returns)
		Strategy_Annualized_Vola.append(Volatility)
		Strategy_Sharpe_Ratio.append(Sharpe)
		Strategy_Composition.append(assets_string)
		Strategy_Weights.append(weights_string)

		#print j

	Results = pd.DataFrame(dict(Strategy_Annualized_Return = Strategy_Annualized_Return, Strategy_Annualized_Vola = Strategy_Annualized_Vola, Strategy_Sharpe_Ratio = Strategy_Sharpe_Ratio, Strategy_Composition = Strategy_Composition, Strategy_Weights = Strategy_Weights)).sort(['Strategy_Annualized_Vola'], ascending=[True]).reset_index(drop=True)
	FilteredResults = Results[(Results["Strategy_Annualized_Return"]>0)].sort_values(['Strategy_Sharpe_Ratio'], ascending=[True]).reset_index(drop=True)
	
	return FilteredResults

	#Results.to_csv(os.getcwd()+"/In_Sample_Optimization_Step"+Increment+".txt")

LMA_DataFrame_New["SelectedAssets"] = 0
LMA_DataFrame_New["SelectedWeights"] = 0
LMA_DataFrame_New["BASE_SelectedAssets"] = 0
LMA_DataFrame_New["BASE_SelectedWeights"] = 0
for i in range(72,529,48):
	print i
	ApplyFrom = i
	ApplyTo = ApplyFrom + 47

	LookBackFrom = i-72
	LookBackTo = LookBackFrom + 71

	Results = MeanVariance(Iterations,LMA_DataFrame,LookBackFrom,LookBackTo,"FULL")
	BASE_Results = MeanVariance(Iterations,LMA_DataFrame,LookBackFrom,LookBackTo,"BASE")

	LMA_DataFrame_New["SelectedAssets"][ApplyFrom-2:ApplyTo-1] = Results["Strategy_Composition"][0]
	LMA_DataFrame_New["SelectedWeights"][ApplyFrom-2:ApplyTo-1] = Results["Strategy_Weights"][0]

	LMA_DataFrame_New["BASE_SelectedAssets"][ApplyFrom-2:ApplyTo-1] = BASE_Results["Strategy_Composition"][0]
	LMA_DataFrame_New["BASE_SelectedWeights"][ApplyFrom-2:ApplyTo-1] = BASE_Results["Strategy_Weights"][0]

LMA_DataFrame_New["Portfolio"] = 0.0
LMA_DataFrame_New["EW_Portfolio"] = 0.0
LMA_DataFrame_New["BASE_Portfolio"] = 0.0
for i in range(0,len(LMA_DataFrame_New)):
	if (LMA_DataFrame_New["SelectedAssets"][i] != 0):
		Assets = LMA_DataFrame_New["SelectedAssets"][i].split(" ")
		Weights = LMA_DataFrame_New["SelectedWeights"][i].split(" ")

		BASE_Assets = LMA_DataFrame_New["BASE_SelectedAssets"][i].split(" ")
		BASE_Weights = LMA_DataFrame_New["BASE_SelectedWeights"][i].split(" ")
		
		for j in range(1,len(Assets)):
			for q in range(1,len(LMA_DataFrame_New.columns)):
				if (LMA_DataFrame_New.columns[q] == Assets[j]):
					LMA_DataFrame_New["Portfolio"][i] = decimal.Decimal(LMA_DataFrame_New["Portfolio"][i]) + decimal.Decimal(Weights[j]) * decimal.Decimal(LMA_DataFrame_New[LMA_DataFrame_New.columns[q]][i])
					LMA_DataFrame_New["EW_Portfolio"][i] = decimal.Decimal(LMA_DataFrame_New["Portfolio"][i]) + decimal.Decimal(1.0/5.0) * decimal.Decimal(LMA_DataFrame_New[LMA_DataFrame_New.columns[q]][i])
				if (LMA_DataFrame_New.columns[q] == BASE_Assets[j]):
					LMA_DataFrame_New["BASE_Portfolio"][i] = decimal.Decimal(LMA_DataFrame_New["BASE_Portfolio"][i]) + decimal.Decimal(BASE_Weights[j]) * decimal.Decimal(LMA_DataFrame_New[LMA_DataFrame_New.columns[q]][i])


Portfolio_Returns =  filter(lambda a: a != 0, LMA_DataFrame_New["Portfolio"].tolist())
EW_Portfolio_Returns =  filter(lambda a: a != 0, LMA_DataFrame_New["EW_Portfolio"].tolist())
BASE_Portfolio_Returns =  filter(lambda a: a != 0, LMA_DataFrame_New["BASE_Portfolio"].tolist())
Portfolio_Equity = []
EW_Portfolio_Equity = []
BASE_Portfolio_Equity = []
for i in range(0,len(Portfolio_Returns)):
	if (i==0):
		Portfolio_Equity.append(100*(1+Portfolio_Returns[i]))
		EW_Portfolio_Equity.append(100*(1+EW_Portfolio_Returns[i]))
		BASE_Portfolio_Equity.append(100*(1+BASE_Portfolio_Returns[i]))
	else:
		Portfolio_Equity.append(Portfolio_Equity[-1]*(1+2*Portfolio_Returns[i]))
		EW_Portfolio_Equity.append(EW_Portfolio_Equity[-1]*(1+2*EW_Portfolio_Returns[i]))
		BASE_Portfolio_Equity.append(BASE_Portfolio_Equity[-1]*(1+2*BASE_Portfolio_Returns[i]))


Sharpe = (np.mean(Portfolio_Returns)*52 - RiskFree) / (np.std(Portfolio_Returns)*math.sqrt(52))
EW_Sharpe = (np.mean(EW_Portfolio_Returns)*52 - RiskFree) / (np.std(EW_Portfolio_Returns)*math.sqrt(52))
BASE_Sharpe = (np.mean(BASE_Portfolio_Returns)*52 - RiskFree) / (np.std(BASE_Portfolio_Returns)*math.sqrt(52))


plt.title("LAM Optimization - Granularity: " + str(Iterations) + " Sharpe: " + str(round(Sharpe,2)))
plt.xlabel("Time Period 01.07.2007.01 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot(Portfolio_Equity, color='k', label="FULL LMA + OPT Allocations - Sharpe: " + str(round(Sharpe,2)))
plt.plot(EW_Portfolio_Equity, color='g', label="FULL LMA + EQ Allocations - Sharpe: " + str(round(EW_Sharpe,2)))
plt.plot(BASE_Portfolio_Equity, color='b', label="BASE LMA + OPT Allocations - Sharpe: " + str(round(BASE_Sharpe,2)))
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
plt.savefig(os.getcwd()+"/NEW/LAM_Plot_"+str(Iterations)+".png", dpi=300)

LMA_DataFrame_New.to_csv(os.getcwd()+"/NEW/In_Sample_Optimization_"+str(Iterations)+".txt")
