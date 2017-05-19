import matplotlib.pylab as plt, os, pandas as pd,  numpy as np, seaborn as sns


category = "DE_LM_AM"
file = "USDJPY"
player = "Asset_Mgr"

database = pd.read_csv(os.getcwd()+"/Output/"+category+"/"+file+"_"+player+"_Output.csv")

if (file=="XAUUSD"):
	multiplier = 10
else:
	multiplier = 1

plt.figure(1).clf()
plt.title(file + " " + player)
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database["Total_Basic_PL"]*multiplier+1000000)/10000, color='k')
plt.savefig(os.getcwd()+"/Equities/BASE_"+file+"_"+player+".png", dpi=300)

plt.figure(2).clf()
plt.title(file + " " + player)
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database["Total_AR_Comb_PL"]*multiplier+1000000)/10000, color='k')
plt.savefig(os.getcwd()+"/Equities/AR_"+file+"_"+player+".png", dpi=300)

plt.figure(3).clf()
plt.title(file + " " + player)
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database["Total_GARCH__PL"]*multiplier+1000000)/10000, color='k')
plt.savefig(os.getcwd()+"/Equities/GARCH_"+file+"_"+player+".png", dpi=300)



# Combinations
database1 = pd.read_csv(os.getcwd()+"/Output/"+"Comm_NonComm"+"/"+"GBPUSD"+"_"+"Comm"+"_Output.csv")
database2 = pd.read_csv(os.getcwd()+"/Output/"+"DE_LM_AM"+"/"+"USDCAD"+"_"+"Asset_Mgr"+"_Output.csv")
database3 = pd.read_csv(os.getcwd()+"/Output/"+"DE_LM_AM"+"/"+"USDJPY"+"_"+"Dealer"+"_Output.csv")
database4 = pd.read_csv(os.getcwd()+"/Output/"+"Comm_NonComm"+"/"+"AUDUSD"+"_"+"NonComm"+"_Output.csv")
database5 = pd.read_csv(os.getcwd()+"/Output/"+"DE_LM_AM"+"/"+"EURUSD"+"_"+"Leverage_Money"+"_Output.csv")

plt.figure(4).clf()
plt.title("BASE Model - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database1["Total_Basic_PL"]*multiplier+1000000)/10000,label="GBPUSD Comm")
plt.plot((database2["Total_Basic_PL"]*multiplier+1000000)/10000,label="USDCAD Asset Manager")
plt.plot((database3["Total_Basic_PL"]*multiplier+1000000)/10000,label="USDJPY Dealer")
plt.plot((database4["Total_Basic_PL"]*multiplier+1000000)/10000,label="AUDUSD NonComm")
plt.plot((database5["Total_Basic_PL"]*multiplier+1000000)/10000,label="EURUSD Leverage Money")
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/Equities/COMB_BASE.png", dpi=300)

plt.figure(5).clf()
plt.title("AR Model - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database1["Total_AR_Comb_PL"]*multiplier+1000000)/10000,label="GBPUSD Comm")
plt.plot((database2["Total_AR_Comb_PL"]*multiplier+1000000)/10000,label="USDCAD Asset Manager")
plt.plot((database3["Total_AR_Comb_PL"]*multiplier+1000000)/10000,label="USDJPY Dealer")
plt.plot((database4["Total_AR_Comb_PL"]*multiplier+1000000)/10000,label="AUDUSD NonComm")
plt.plot((database5["Total_AR_Comb_PL"]*multiplier+1000000)/10000,label="EURUSD Leverage Money")
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/Equities/COMB_AR.png", dpi=300)

plt.figure(6).clf()
plt.title("GARCH Model - Cum. Returns (Indexed)")
plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
plt.ylabel("Index")
plt.plot((database1["Total_GARCH__PL"]*multiplier+1000000)/10000,label="GBPUSD Comm")
plt.plot((database2["Total_GARCH__PL"]*multiplier+1000000)/10000,label="USDCAD Asset Manager")
plt.plot((database3["Total_GARCH__PL"]*multiplier+1000000)/10000,label="USDJPY Dealer")
plt.plot((database4["Total_GARCH__PL"]*multiplier+1000000)/10000,label="AUDUSD NonComm")
plt.plot((database5["Total_GARCH__PL"]*multiplier+1000000)/10000,label="EURUSD Leverage Money")
plt.legend(loc='upper left', prop={'size':8})
plt.savefig(os.getcwd()+"/Equities/COMB_GARCH.png", dpi=300)







