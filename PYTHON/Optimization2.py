# https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

import pandas as pd, os, logging, scipy.stats as stats, pyflux as pf, math, seaborn as sns
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from datetime import datetime, timedelta
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from scipy.stats import gaussian_kde


logging.basicConfig(filename='Log.txt',level=logging.DEBUG)

def DickeyFuller_Test(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    #orig = plt.plot(timeseries, color='blue',label='Original')
    #mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    #std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    #plt.legend(loc='best')
    #plt.title('Rolling Mean & Standard Deviation')
    #plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput

def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total

category = "DE_LM_AM"
file = "AUDUSD"
player = "Asset_Mgr"
plots = 'ON'

SignalDirectory = os.getcwd()+"/Databases/" + category + "/" + file +".csv"
PlotsDirectory = os.getcwd()+"/Plots/" + category + "/" + file + "/"
OutputDirectory = os.getcwd() + "/Output/" + category + "/"
OptionsDirectory = os.getcwd()+"/Databases/OptionsDatabase.csv"

logging.info('\t'+str(datetime.now())+'	Loading Instrument Database...')
Instrument_Data = pd.read_csv(SignalDirectory)
Instrument_Data["As_of_Date_In_Form_YYMMDD"] = pd.to_datetime(Instrument_Data["As_of_Date_In_Form_YYMMDD"])

Instrument_Data["Trade_Date"] = Instrument_Data["As_of_Date_In_Form_YYMMDD"].dt.to_period('W').apply(lambda r: r.start_time) + timedelta(days=7)

logging.info('\t'+str(datetime.now())+'	Loading Pricing Database...')
Pricing_Data = pd.read_csv(OptionsDirectory,delimiter=";")
Pricing_Data["Trade_Date"] = pd.to_datetime(Pricing_Data["Trade_Date"], format='%d.%m.%Y')
for column in Pricing_Data:
    if "CALL_" in column or "PUT_" in column:
    	if file not in column:
    		del Pricing_Data[column]

# Merge DataFrames
logging.info('\t'+str(datetime.now())+'	Matching Instrument & Pricing Database...')
Instrument_Data = pd.merge(Instrument_Data, Pricing_Data, on='Trade_Date', how='inner')

# Calculate Week-over-Week Change (%)
logging.info('\t'+str(datetime.now())+'	Calculating Returns...')
ts_ret = np.asarray((Instrument_Data[player+"_Diff"] - Instrument_Data[player+"_Diff"].shift(1))[1:])
Instrument_Data["Returns"] = [0] + ts_ret.tolist()

ts_ret2 = pd.DataFrame( (Instrument_Data[player+"_Diff"] - Instrument_Data[player+"_Diff"].shift(1))[1:].tolist() )
ts_ret2.index = Instrument_Data["Trade_Date"][1:len(ts_ret2)+1]
ts_ret2.columns = ['Returns']

# Conduct DickeyFuller Test on the Series Returns
logging.info('\t'+str(datetime.now())+'	Running Dickey-Fuller Test...')
DickeyFuller_Test(ts_ret)

# Calculate ACF / PACF
logging.info('\t'+str(datetime.now())+'	Calculate ACF/PACF...')
lag_acf = acf(ts_ret, nlags=5)
lag_pacf = pacf(ts_ret, nlags=5, method='ols')

#############################	BASE MODEL #############################
logging.info('\t'+str(datetime.now())+'	Calculating BASE Model...')
Instrument_Data["Basic_PL"] = 0
Instrument_Data['Basic_PL'] = Instrument_Data.apply(lambda x: x["PUT_"+file] if x[player+"_Diff"] > 0 else x["CALL_"+file] if x[player+"_Diff"] < 0 else 0, axis=1)
Instrument_Data['Total_Basic_PL'] = list(accumu(Instrument_Data['Basic_PL'].tolist()))

plt.figure(10).clf()
plt.title(file + " " + player + " ")
plt.xlabel("Time Period 01.01.2006.01 to 31.12.2016 [weeks]")
plt.ylabel("Positioning (% Points)")
pos_signal = (Instrument_Data[player+"_Diff"]*100.0).copy()
neg_signal = (Instrument_Data[player+"_Diff"]*100.0).copy()
pos_signal[pos_signal <= 0] = np.nan
neg_signal[neg_signal > 0] = np.nan
plt.plot(Instrument_Data[player+"_Diff"]*100.0, color='k', label="Positioning")
plt.plot(pos_signal, 'go', color='g', markersize=3, label="BUY Signal")
plt.plot(neg_signal, 'ro', color='r', markersize=3, label="SELL Signal")
plt.legend(loc='lower right', prop={'size':8})
plt.savefig(PlotsDirectory + "/" + player + "_BASE_Model.png", dpi=300)

plt.figure(11).clf()
plt.title(file + " " + player + " ")
plt.xlabel("Time Period 01.01.2006.01 to 31.12.2016 [weeks]")
plt.ylabel("Positioning (% Points)")
pos_signal = (Instrument_Data[player+"_Diff"]*100.0).copy()
neg_signal = (Instrument_Data[player+"_Diff"]*100.0).copy()
pos_signal[pos_signal < 10] = np.nan
neg_signal[neg_signal > -10] = np.nan
plt.plot(Instrument_Data[player+"_Diff"]*100.0, color='k', label="Positioning")
plt.plot(pos_signal, 'go', color='g', markersize=3, label="BUY Signal")
plt.plot(neg_signal, 'ro', color='r', markersize=3, label="SELL Signal")
plt.axhline(y=-10,linestyle='--',color='gray')
plt.axhline(y=10,linestyle='--',color='gray')
plt.legend(loc='lower right', prop={'size':8})
plt.savefig(PlotsDirectory + "/" + player + "_AR_Model.png", dpi=300)

########################################################################


#############################	AR MODEL #############################
logging.info('\t'+str(datetime.now())+'	Calculating AR Model...')
model = ARIMA(ts_ret[:len(ts_ret)/2+1], order=(1,0,0))  
results_AR = model.fit(disp=0)
AR_Pred = results_AR.fittedvalues.tolist()

logging.info('\t'+str(datetime.now())+'	Out of Sample Fitting & Prediction - Returns...')
for i in range(len(ts_ret)/2-1,len(ts_ret)-1):
	# Fit Model again and make prediction
	next_forecast = ARIMA(ts_ret[:i], order=(1,0,0)).fit(disp=0).forecast()[0][0]
	AR_Pred.append(next_forecast)

Instrument_Data["AR_Forecast_Returns"] = AR_Pred
Instrument_Data["AR_Forecast_Diff"] = Instrument_Data[player+"_Diff"]*(1+Instrument_Data["AR_Forecast_Returns"])

# Optimization
Instrument_Data["AR_Comb_Forecast"] = 0
Instrument_Data["AR_Comb_PL"] = 0
Maximum_EQ = -10000000
Maximum_Weight = 0

for weight in range(0,100):
	Instrument_Data["AR_Comb_Forecast"] = Instrument_Data[player+"_Diff"].shift(1)*weight/100.0 + Instrument_Data["AR_Forecast_Diff"]*(1-weight/100.0)

	Instrument_Data['AR_Comb_PL'] = Instrument_Data.apply(lambda x: x["PUT_"+file] if x["AR_Comb_Forecast"] > 0.1 else x["CALL_"+file] if x["AR_Comb_Forecast"] < -0.1 else 0, axis=1)
	Instrument_Data['Total_AR_Comb_PL'] = list(accumu(Instrument_Data['AR_Comb_PL'].tolist()))

	if Instrument_Data['Total_AR_Comb_PL'][275] > Maximum_EQ:
		#plt.plot(Instrument_Data['Total_ARIMA_PL'])
		Maximum_Weight = weight
		Maximum_EQ = Instrument_Data['Total_AR_Comb_PL'][275]

Instrument_Data["AR_Comb_Forecast"] = Instrument_Data[player+"_Diff"].shift(1)*Maximum_Weight/100.0 + Instrument_Data["AR_Forecast_Diff"]*(1-Maximum_Weight/100.0)
Instrument_Data['AR_Comb_PL'] = Instrument_Data.apply(lambda x: x["PUT_"+file] if x["AR_Comb_Forecast"] > 0.1 else x["CALL_"+file] if x["AR_Comb_Forecast"] < -0.1 else 0, axis=1)
Instrument_Data['Total_AR_Comb_PL'] = list(accumu(Instrument_Data['AR_Comb_PL'].tolist()))

print "AR Model" + "\tOptimimal Weight: " + str(Maximum_Weight) + "\tMax Equity: " + str(Maximum_EQ)
#########################################################################


#############################	GARCH MODEL #############################
logging.info('\t'+str(datetime.now())+'	Calculating GARCH Model...')
model1 = pf.GARCH(ts_ret2[:len(ts_ret2)/2+1],p=1,q=1)
results_GR = model1.fit()
results_GR.summary()

# Plot Fit in In-Sample Fitting
model1.plot_fit()

GARCH_Pred = np.sqrt(results_GR.signal).tolist()

for i in range(len(ts_ret2)/2-1,len(ts_ret2)-1):
	# Fit Model again and make prediction
	model2 = pf.GARCH(ts_ret2[:i],p=1,q=1)
	results_GR2 = model2.fit()

	#print model2.predict(h=1)

	Next_GARCH_Forecast = math.sqrt(model2.predict(h=1)["Returns"][ts_ret2.index[i]])
	print str(i) + "	" + str(Next_GARCH_Forecast)
	#print Next_GARCH_Forecast["Series"][i]
	GARCH_Pred.append(Next_GARCH_Forecast)
	
Instrument_Data["Forecast_Volatility"] = [0] + GARCH_Pred
Instrument_Data['hvol21'] = np.sqrt(pd.rolling_std(np.abs(Instrument_Data["Returns"]), 4)*(52**0.5))/2
Instrument_Data["GARCH_PL"] = 0
std_vol = Instrument_Data['Forecast_Volatility'][0:274].mean()
Instrument_Data['GARCH_PL'] = Instrument_Data.apply(lambda x: x["PUT_"+file] if x[player+"_Diff"] > 0 and x['hvol21']>x['Forecast_Volatility'] else x["CALL_"+file] if x[player+"_Diff"] < 0 and x['hvol21']>x['Forecast_Volatility'] else 0, axis=1)
Instrument_Data['Total_GARCH__PL'] = list(accumu(Instrument_Data['GARCH_PL'].tolist()))
#########################################################################

print "Finished Equities Calc"
Instrument_Data.to_csv(OutputDirectory + file + "_" + player + '_Output.csv')

if plots == 'ON':

	#PLOTS
	logging.info('\t'+str(datetime.now()) + '	Plotting...')

	plt.figure(1).clf()
	plt.subplot(2, 1, 1)
	plt.title(file + " " + player + " ")
	plt.ylabel("Positioning (% Points)")
	plt.plot(Instrument_Data[player+"_Diff"]*100.0, color="black",linewidth=1)
	plt.subplot(2, 1, 2)
	plt.xlabel("Time Period 01.01.2006 to 31.12.2016 [weeks]")
	plt.ylabel("Returns (% Points)")
	plt.bar(range(len(ts_ret)),ts_ret*100.0, color="black")
	plt.savefig(PlotsDirectory + "/" + player + "_Positioning_&_Returns.png", dpi=300)

	plt.figure(2).clf()
	plt.title(file + " " + player)
	plt.xlabel("Observed Returns")
	plt.ylabel("Density")
	pdf = stats.norm.pdf(ts_ret2, ts_ret2.mean(), ts_ret2.std())
	plt.plot(ts_ret2, pdf,'.',color="black", label='Normal Density')
	ax = sns.distplot(ts_ret, hist=False, label='Empirical Density', color="black")
	plt.plot(ax.collections, linewidth=1,color="gray")
	plt.legend(loc='upper left', prop={'size':8})
	plt.savefig(PlotsDirectory + "/" + player + "_PDF.png", dpi=300)

	plt.figure(3).clf()
	#Plot ACF: 
	plt.subplot(121) 
	plt.plot(lag_acf,color="black")
	plt.axhline(y=0,linestyle='--',color='gray')
	plt.xlabel("Lags")
	plt.ylabel("Correlation")
	# Add confidence 95%interval
	plt.axhline(y=-1.96/np.sqrt(len(ts_ret)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(ts_ret)),linestyle='--',color='gray')
	plt.title('Autocorrelation Function')
	#Plot PACF:
	plt.subplot(122)
	plt.plot(lag_pacf,color="black")
	plt.xlabel("Lags")
	plt.ylabel("Correlation")
	plt.axhline(y=0,linestyle='--',color='gray')
	# Add confidence 95%interval
	plt.axhline(y=-1.96/np.sqrt(len(ts_ret)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(ts_ret)),linestyle='--',color='gray')
	plt.title('Partial Autocorrelation Function')
	plt.tight_layout()
	plt.savefig(PlotsDirectory  + "/" + player + "_ACF_PACF.png", dpi=300)

	plt.figure(4).clf()
	plt.title(file + " " + player + " ")
	plt.xlabel("Time Period 01.01.2006.01 to 31.12.2016 [weeks]")
	plt.ylabel("Returns (% Points)")
	plt.plot(ts_ret, label='Returns')
	plt.plot(AR_Pred, color='red', label='AR Pred.')
	plt.axvline(x=len(ts_ret)/2, color='k', linestyle='--')
	plt.legend(loc='upper left', prop={'size':8})
	plt.savefig(PlotsDirectory + "/" + player + "_AR_Fitted.png", dpi=300)

	plt.figure(5).clf()
	plt.title("Strategy Equities")
	plt.xlabel("Period")
	plt.ylabel("Equity")
	plt.plot(Instrument_Data['Total_Basic_PL'], label='Base Model')
	plt.plot(Instrument_Data['Total_AR_Comb_PL'], label='AR Model')
	plt.plot(Instrument_Data['Total_GARCH__PL'], label='GARCH Model')
	plt.axvline(x=len(ts_ret)/2, color='k', linestyle='--')
	plt.legend(loc='upper left', prop={'size':8})
	plt.savefig(PlotsDirectory + "/" + player + "_Equities.png", dpi=300)

	plt.figure(6).clf()
	plt.title(file + " " + player + " ")
	plt.xlabel("Time Period 01.01.2006.01 to 31.12.2016 [weeks]")
	plt.ylabel("Conditional Volatility (% Points)")
	plt.plot(np.abs(ts_ret2['Returns'].tolist()), label='Volatility')
	plt.plot(GARCH_Pred, color='red', label='GARCH Pred.')
	plt.axvline(x=len(ts_ret2)/2, color='k', linestyle='--')
	plt.legend(loc='upper left', prop={'size':8})
	plt.savefig(PlotsDirectory + "/" + player + "_GARCH.png", dpi=300)

















