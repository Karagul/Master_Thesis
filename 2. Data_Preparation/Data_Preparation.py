import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os, numpy, datetime


#Load Settings File
databasePath1 = os.getcwd() + "/databases/CFTC_database/FinFut.txt"
InstrumetnsOfInterest1 = ["CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE", "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE", "BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE", "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE", "EURO FX - CHICAGO MERCANTILE EXCHANGE", "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE", "RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE", "MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE", "BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE", "NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE", "S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE", "U.S. TREASURY BONDS - CHICAGO BOARD OF TRADE", "10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF TRADE", "U.S. DOLLAR INDEX - ICE FUTURES U.S."]

databasePath2 = os.getcwd() + "/databases/CFTC_database/DeaFut.txt"
InstrumetnsOfInterest2 = ["2-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF TRADE","10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF TRADE","5-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF TRADE","PALLADIUM - NEW YORK MERCANTILE EXCHANGE","SILVER - COMMODITY EXCHANGE INC.","COPPER-GRADE #1 - COMMODITY EXCHANGE INC.","GOLD - COMMODITY EXCHANGE INC.","CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE","SWISS FRANC - CHICAGO MERCANTILE EXCHANGE","MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE","BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE","JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE","U.S. DOLLAR INDEX - NEW YORK BOARD OF TRADE","EURO FX - CHICAGO MERCANTILE EXCHANGE","UNLEADED GASOLINE, N.Y. HARBOR - NEW YORK MERCANTILE EXCHANGE","NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE","DOW JONES INDUSTRIAL AVERAGE - CHICAGO BOARD OF TRADE","S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE","NASDAQ-100 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE","AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE","WTI CRUDE OIL FINANCIAL - NEW YORK MERCANTILE EXCHANGE","U.S. DOLLAR INDEX - ICE FUTURES U.S.","RUSSIAN RUBLE - CHICAGO MERCANTILE EXCHANGE","CRUDE OIL, LIGHT SWEET - ICE EUROPE","BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE","BRENT CRUDE OIL LAST DAY - NEW YORK MERCANTILE EXCHANGE","CRUDE OIL, LIGHT SWEET-WTI - ICE FUTURES EUROPE","WTI-BRENT CALENDAR SWAP - NEW YORK MERCANTILE EXCHANGE","EURO FX/BRITISH POUND XRATE - CHICAGO MERCANTILE EXCHANGE"]


data1 = pd.read_csv(databasePath1, sep="\t")
data2 = pd.read_csv(databasePath2, sep="\t")

text_file = open(os.getcwd() + "/OutputInformation.txt", "w")



# FinFut - Loop through instruments
for i in range(0,len(InstrumetnsOfInterest1)):
	
	# Filter data1base
	Filtereddatabase = data1[data1['Market_and_Exchange_Names'].str.contains(InstrumetnsOfInterest1[i])].sort(["As_of_Date_In_Form_YYMMDD"]).reset_index(drop=True)

	Filtereddatabase["As_of_Date_In_Form_YYMMDD"] = [datetime.datetime.strptime(date, '%Y%m%d').date() for date in ['20'+x  for x in [ '%0.6d' % x for x in map(int, numpy.asarray(Filtereddatabase["As_of_Date_In_Form_YYMMDD"]))]]]
	
	# LEVERAGE MONEY
	Filtereddatabase['Leverage_Money_Pos'] = Filtereddatabase['Lev_Money_Positions_Long_All'] - Filtereddatabase['Lev_Money_Positions_Short_All']
	Filtereddatabase['Leverage_Money_Diff'] = (Filtereddatabase['Lev_Money_Positions_Long_All'] / (Filtereddatabase['Lev_Money_Positions_Long_All'] + Filtereddatabase['Lev_Money_Positions_Short_All']) - Filtereddatabase['Lev_Money_Positions_Short_All'] / (Filtereddatabase['Lev_Money_Positions_Long_All'] + Filtereddatabase['Lev_Money_Positions_Short_All']))
	Filtereddatabase['Leverage_Money_Signal1'] = np.where((Filtereddatabase['Lev_Money_Positions_Long_All'] / (Filtereddatabase['Lev_Money_Positions_Long_All'] + Filtereddatabase['Lev_Money_Positions_Short_All']) - Filtereddatabase['Lev_Money_Positions_Short_All'] / (Filtereddatabase['Lev_Money_Positions_Long_All'] + Filtereddatabase['Lev_Money_Positions_Short_All']))>0.0, 'SHORT', 'LONG')

	# DEALERS
	Filtereddatabase['Dealer_Pos'] = Filtereddatabase['Dealer_Positions_Long_All'] - Filtereddatabase['Dealer_Positions_Short_All']
	Filtereddatabase['Dealer_Diff'] = (Filtereddatabase['Dealer_Positions_Long_All'] / (Filtereddatabase['Dealer_Positions_Long_All'] + Filtereddatabase['Dealer_Positions_Short_All']) - Filtereddatabase['Dealer_Positions_Short_All'] / (Filtereddatabase['Dealer_Positions_Long_All'] + Filtereddatabase['Dealer_Positions_Short_All']))
	Filtereddatabase['Dealer_Signal1'] = np.where((Filtereddatabase['Dealer_Positions_Long_All'] / (Filtereddatabase['Dealer_Positions_Long_All'] + Filtereddatabase['Dealer_Positions_Short_All']) - Filtereddatabase['Dealer_Positions_Short_All'] / (Filtereddatabase['Dealer_Positions_Long_All'] + Filtereddatabase['Dealer_Positions_Short_All']))>0.0, 'SHORT', 'LONG')

	# ASSET MANAGERS
	Filtereddatabase['Asset_Mgr_Pos'] = Filtereddatabase['Asset_Mgr_Positions_Long_All'] - Filtereddatabase['Asset_Mgr_Positions_Short_All']
	Filtereddatabase['Asset_Mgr_Diff'] = (Filtereddatabase['Asset_Mgr_Positions_Long_All'] / (Filtereddatabase['Asset_Mgr_Positions_Long_All'] + Filtereddatabase['Asset_Mgr_Positions_Short_All']) - Filtereddatabase['Asset_Mgr_Positions_Short_All'] / (Filtereddatabase['Asset_Mgr_Positions_Long_All'] + Filtereddatabase['Asset_Mgr_Positions_Short_All']))
	Filtereddatabase['Asset_Mgr_Signal1'] = np.where((Filtereddatabase['Asset_Mgr_Positions_Long_All'] / (Filtereddatabase['Asset_Mgr_Positions_Long_All'] + Filtereddatabase['Asset_Mgr_Positions_Short_All']) - Filtereddatabase['Asset_Mgr_Positions_Short_All'] / (Filtereddatabase['Asset_Mgr_Positions_Long_All'] + Filtereddatabase['Asset_Mgr_Positions_Short_All']))<0.0, 'SHORT', 'LONG')

	# Propageate forward for any missing values
	Filtereddatabase.fillna(method='ffill', inplace=True)


	# SAVE INSTRUMENT INFORMATION
	text_file.write("Instrument:" + "\t" + InstrumetnsOfInterest1[i].split(" - ")[0].replace("/","-") + "\t" + " Entries:" + "\t" + str(len(Filtereddatabase)) + "\t" + "StartDate:"+ "\t" + str(Filtereddatabase["As_of_Date_In_Form_YYMMDD"][0]) + "\t" + "EndDate:" + "\t" + str(Filtereddatabase["As_of_Date_In_Form_YYMMDD"][len(Filtereddatabase)-1]) + "\t" + "Database"+ "\t" + "FinFut" + "\n")

	# SAVE FILE
	Filtereddatabase.to_csv(os.getcwd()+"/Signals/FinFut/"+InstrumetnsOfInterest1[i].split(" - ")[0].replace("/","-") +".csv")

	#if InstrumetnsOfInterest2[i] == "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE":
	#	plt.plot(Filtereddatabase['Lev_Money_Positions_Long_All']-Filtereddatabase['Lev_Money_Positions_Short_All'])
	#	plt.plot(Filtereddatabase['Dealer_Positions_Long_All']-Filtereddatabase['Dealer_Positions_Short_All'])
	#	plt.plot(Filtereddatabase['Asset_Mgr_Positions_Long_All']-Filtereddatabase['Asset_Mgr_Positions_Short_All'])
	#	plt.show();

# DeaFut - Loop through instruments
for i in range(0,len(InstrumetnsOfInterest2)):
	# Filter data1base
	Filtereddatabase = data2[data2['Market_and_Exchange_Names'].str.contains(InstrumetnsOfInterest2[i])].sort(["As_of_Date_In_Form_YYMMDD"]).reset_index(drop=True)

	Filtereddatabase["As_of_Date_In_Form_YYMMDD"] = [datetime.datetime.strptime(date, '%Y%m%d').date() for date in ['20'+x  for x in [ '%0.6d' % x for x in map(int, numpy.asarray(Filtereddatabase["As_of_Date_In_Form_YYMMDD"]))]]]

	# NON-COMMERCIALS
	Filtereddatabase['NonComm_Pos'] = Filtereddatabase['NonComm_Positions_Long_All'] - Filtereddatabase['NonComm_Positions_Short_All']
	Filtereddatabase['NonComm_Diff'] = (Filtereddatabase['NonComm_Positions_Long_All'] / (Filtereddatabase['NonComm_Positions_Long_All'] + Filtereddatabase['NonComm_Positions_Short_All']) - Filtereddatabase['NonComm_Positions_Short_All'] / (Filtereddatabase['NonComm_Positions_Long_All'] + Filtereddatabase['NonComm_Positions_Short_All']))
	Filtereddatabase['NonComm_Signal1'] = np.where((Filtereddatabase['NonComm_Positions_Long_All'] / (Filtereddatabase['NonComm_Positions_Long_All'] + Filtereddatabase['NonComm_Positions_Short_All']) - Filtereddatabase['NonComm_Positions_Short_All'] / (Filtereddatabase['NonComm_Positions_Long_All'] + Filtereddatabase['NonComm_Positions_Short_All']))>0.0, 'SHORT', 'LONG')

	# COMMERCIALS
	Filtereddatabase['Comm_Pos'] = Filtereddatabase['Comm_Positions_Long_All'] - Filtereddatabase['Comm_Positions_Short_All']
	Filtereddatabase['Comm_Diff'] = (Filtereddatabase['Comm_Positions_Long_All'] / (Filtereddatabase['Comm_Positions_Long_All'] + Filtereddatabase['Comm_Positions_Short_All']) - Filtereddatabase['Comm_Positions_Short_All'] / (Filtereddatabase['Comm_Positions_Long_All'] + Filtereddatabase['Comm_Positions_Short_All']))
	Filtereddatabase['Comm_Signal1'] = np.where((Filtereddatabase['Comm_Positions_Long_All'] / (Filtereddatabase['Comm_Positions_Long_All'] + Filtereddatabase['Comm_Positions_Short_All']) - Filtereddatabase['Comm_Positions_Short_All'] / (Filtereddatabase['Comm_Positions_Long_All'] + Filtereddatabase['Comm_Positions_Short_All']))>0.0, 'SHORT', 'LONG')

	# Propageate forward for any missing values
	Filtereddatabase.fillna(method='ffill', inplace=True)

	# SAVE INSTRUMENT INFORMATION
	text_file.write("Instrument:" + "\t" + InstrumetnsOfInterest2[i].split(" - ")[0].replace("/","-") + "\t" + " Entries:" + "\t" + str(len(Filtereddatabase)) + "\t" + "StartDate:"+ "\t" + str(Filtereddatabase["As_of_Date_In_Form_YYMMDD"][0]) + "\t" + "EndDate:" + "\t" + str(Filtereddatabase["As_of_Date_In_Form_YYMMDD"][len(Filtereddatabase)-1]) + "\t" + "Database"+ "\t" + "DeaFut" + "\n")

	# SAVE FILE
	Filtereddatabase.to_csv(os.getcwd()+"/Signals/DeaFut/"+InstrumetnsOfInterest2[i].split(" - ")[0].replace("/","-") +".csv")


	
text_file.close()








