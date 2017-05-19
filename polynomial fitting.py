import pandas as pd, os, numpy, datetime, matplotlib.pyplot as plt

symbolname = "EURO FX"
symbol = "EURUSD"
player = ["Asset_Mgr","Dealer","Leverage_Money"]
#player = ["NonComm","Comm"]
polyfit_intervals = [4,6,8,10,12,25,50]
polyfit_degree = 6

# Load Option P/Ls
Options_Data = pd.read_csv(os.getcwd()+"/Databases/Options/Options_Database.csv")
Options_Data["Trade_Date"] =  [datetime.datetime.strptime(date, '%d.%m.%y').date() for date in Options_Data["Trade_Date"]]

for j in range(0,len(player)):
	for u in range(0,len(polyfit_intervals)):
		# Load data
		data = pd.read_csv(os.getcwd()+"/Signals/FinFut/"+symbolname+".csv")

		# Create DataFrame where analysis will take place
		dataframe = pd.DataFrame()

		for i in range (0,len(data.columns)):
			if data.columns[i] == ("As_of_Date_In_Form_YYMMDD"):
				dataframe["Data_Date"] = [datetime.datetime.strptime(date, '%Y%m%d').date() for date in ['20'+x  for x in [ '%0.6d' % x for x in map(int, numpy.asarray(data[data.columns[i]]))]]]
			if data.columns[i] == (player[j]+"_Diff"):
				dataframe["Positioning_Diff"] = map(float, numpy.asarray(data[data.columns[i]]))
			if data.columns[i] == (player[j]+"_Signal1"):
				dataframe["Signal"] = map(str, numpy.asarray(data[data.columns[i]]))

		dataframe["Trade_Date"] =  [x + datetime.timedelta(days=(7 - x.weekday())) for x in dataframe["Data_Date"]]

		# Merge Dataframes to have signals and P/Ls in the same dataframe
		dataframe = pd.merge(dataframe, Options_Data, left_on = 'Trade_Date', right_on = 'Trade_Date')

		# Determine weekly P/L of signal according to Positioning
		dataframe["Signal_PL"] = numpy.where(dataframe['Signal']=='SHORT', dataframe[symbol+"_CALL"], dataframe[symbol+"_PUT"])

		# Calculate Total P/L of Signal
		s = (numpy.cumsum([0]+dataframe["Signal_PL"][:-1]).tolist())
		s.append(s[len(s)-1] + dataframe["Signal_PL"][len(dataframe)-1])
		dataframe["Signal_Total_PL"] = s



		# Fitting Data

		Split_Database = numpy.array_split(dataframe, polyfit_intervals[u])


		for i in range(0,polyfit_intervals[u]):
			
			if i==0:
				p = numpy.poly1d(numpy.polyfit(Split_Database[i]["Positioning_Diff"],Split_Database[i]["Signal_PL"],polyfit_degree))
				Split_Database[i]["Fitted_PL"] = p(Split_Database[i]["Positioning_Diff"])

				p = numpy.poly1d(numpy.polyfit(Split_Database[i]["Positioning_Diff"],Split_Database[i]["Signal_PL"],polyfit_degree))
				Split_Database[i]["Fitted_PL_Forward"] = p(Split_Database[i]["Positioning_Diff"])

				bigdata = Split_Database[i]
			else:
				p = numpy.poly1d(numpy.polyfit(Split_Database[i]["Positioning_Diff"],Split_Database[i]["Signal_PL"],polyfit_degree))
				Split_Database[i]["Fitted_PL"] = p(Split_Database[i]["Positioning_Diff"])

				p = numpy.poly1d(numpy.polyfit(Split_Database[i-1]["Positioning_Diff"],Split_Database[i-1]["Signal_PL"],polyfit_degree))
				Split_Database[i]["Fitted_PL_Forward"] = p(Split_Database[i]["Positioning_Diff"])

				bigdata = bigdata.append(Split_Database[i], ignore_index=True)


		s = (numpy.cumsum([0]+bigdata["Fitted_PL"][:-1]).tolist())
		s.append(s[len(s)-1] + bigdata["Fitted_PL"][len(bigdata)-1])
		bigdata["Signal_Total_PL_Fitted"] = s

		bigdata["Fitted_PL_Rule_Weight"] = [0 if x <=0 else 0.5 if x <1000 else 1 for x in bigdata["Fitted_PL"]]
		bigdata["Fitted_PL_Rule_Adj"] = bigdata["Signal_PL"]*bigdata["Fitted_PL_Rule_Weight"]
		s = (numpy.cumsum([0]+bigdata["Fitted_PL_Rule_Adj"][:-1]).tolist())
		s.append(s[len(s)-1] + bigdata["Fitted_PL_Rule_Adj"][len(bigdata)-1])
		bigdata["Signal_Total_PL_Fitted_Rule"] = s


#[0 if x <=0 else 0.5 if x <1000 else 1 for x in bigdata["Fitted_PL_Forward"]]
		bigdata["Fitted_PL_Forward_Rule_Weight"] = [1 for x in bigdata["Fitted_PL_Forward"]]
		bigdata["Fitted_PL_Forward_Rule_Adj"] = bigdata["Signal_PL"]*bigdata["Fitted_PL_Forward_Rule_Weight"]
		s = (numpy.cumsum([0]+bigdata["Fitted_PL_Forward_Rule_Adj"][:-1]).tolist())
		s.append(s[len(s)-1] + bigdata["Fitted_PL_Forward_Rule_Adj"][len(bigdata)-1])
		bigdata["Fitted_Total_PL_Forward_Fitted_Rule"] = s


		plt.title(symbol + " " + player[j] + " " + str(polyfit_intervals[u]) +" int")
		plt.xlabel("Date")
		plt.ylabel("P/L")
		plt.plot(bigdata["Trade_Date"],bigdata["Signal_Total_PL"],label="Original Equity")
		plt.plot(bigdata["Trade_Date"],bigdata["Signal_Total_PL_Fitted"],label="Fitted Equity")
		plt.plot(bigdata["Trade_Date"],bigdata["Signal_Total_PL_Fitted_Rule"],label="Fitted Equity + Rule")
		plt.plot(bigdata["Trade_Date"],bigdata["Fitted_Total_PL_Forward_Fitted_Rule"],label="Forward Look + Rule")
		plt.legend(loc='upper left', prop={'size':8})

		plt.savefig(os.getcwd()+'/Output/'+symbol +"/"+str(polyfit_intervals[u])+"/"+symbol+" "+player[j]+" "+str(polyfit_intervals[u])+"int.png",dpi = 300)
		plt.close()

		bigdata.to_csv(os.getcwd()+'/Output/'+symbol+"/"+str(polyfit_intervals[u])+"/"+symbol+" "+player[j]+" "+str(polyfit_intervals[u])+"int.csv")



