% Define  File to Load
% WIndows
%filename = 'C:\Users\Jannis\Dropbox\Master_Thesis\MATLAB\Databases/JAPANESE YEN.csv';
% Mac
filename = '/Users/MacMini1/Dropbox/Master_Thesis/MATLAB/Databases/JAPANESE YEN.csv';

% Select Number of players
p = 3;
Players = {'Dealer','Asset_Mgr','Leverage_Money'};

% Load FIle
Database = ImportDataFunctionTable(filename, 2, inf );

% Calculate Trade Date
Database.Trade_Date = dateshift(Database.As_of_Date_In_Form_YYMMDD,'dayofweek','Monday');

% Calculate Positioning Differences
Database.Asset_Mgr_Diff = (Database.Asset_Mgr_Positions_Long_All-Database.Asset_Mgr_Positions_Short_All)./(Database.Asset_Mgr_Positions_Long_All+Database.Asset_Mgr_Positions_Short_All);
Database.Lev_Money_Diff = (Database.Lev_Money_Positions_Long_All-Database.Lev_Money_Positions_Short_All)./(Database.Lev_Money_Positions_Long_All+Database.Lev_Money_Positions_Short_All);
Database.Dealer_Diff = (Database.Dealer_Positions_Long_All-Database.Dealer_Positions_Short_All)./(Database.Dealer_Positions_Long_All+Database.Dealer_Positions_Short_All);

% Calculate Returns
%Database.Asset_Mgr_Ret = zeros(size(Database,1), 1);
%Database.Lev_Money_Ret = zeros(size(Database,1), 1);
%Database.Dealer_Ret = zeros(size(Database,1), 1);
%Database.Asset_Mgr_Ret(2:end) = price2ret(Database.Asset_Mgr_Diff+10);
%Database.Lev_Money_Ret(2:end) = price2ret(Database.Lev_Money_Diff+10);
%Database.Dealer_Ret(2:end) = price2ret(Database.Dealer_Diff+10);

% Determine AIC/BIC parameters
%[bestAIC,bestBIC]=select_model(Database.Asset_Mgr_Ret,4,1,1,1);

% Create Model
%ToEstVarMdl1 = garch(0,0);
%ToEstMdl11 = arima('ARLags',1,'MALags',1,'Variance',ToEstVarMdl1);
ToEstMdl11 = arima(1,0,1);


Database.Asset_Mgr_Diff_Pred = zeros(size(Database,1), 1);
Database.Lev_Money_Diff_Pred = zeros(size(Database,1), 1);
Database.Dealer_Diff_Pred = zeros(size(Database,1), 1);

%Database.AR = zeros(size(Database,1), 1);
%Database.MA = zeros(size(Database,1), 1);


%Residuals = infer(EstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:));
ToEstMdl11 = arima(1,0,1);
[EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:),'print',false);
Asset_Mgr_Est_Data = Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:));

[EstMdl11,EstParamCov12,logl12] = estimate(ToEstMdl11,Database.Lev_Money_Diff(1:round(size(Database,1)/2),:),'print',false);
Lev_Money_Est_Data = Database.Lev_Money_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl11,Database.Lev_Money_Diff(1:round(size(Database,1)/2),:));

[EstMdl11,EstParamCov13,logl13] = estimate(ToEstMdl11,Database.Dealer_Diff(1:round(size(Database,1)/2),:),'print',false);
Dealer_Est_Data = Database.Dealer_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl11,Database.Dealer_Diff(1:round(size(Database,1)/2),:));

for i = 1:round(size(Database,1)/2)
    Database.Asset_Mgr_Diff_Pred(i,:) = Asset_Mgr_Est_Data(i,:);
    Database.Lev_Money_Diff_Pred(i,:) = Lev_Money_Est_Data(i,:);
    Database.Dealer_Diff_Pred(i,:) = Dealer_Est_Data(i,:);
end




for i = round(size(Database,1)/2):(size(Database,1)-1)
    %[EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Asset_Mgr_Ret(2:i,:),'print',false);
    %Database.AR(i,:) = EstMdl11.AR{1};
    %Database.MA(i,:) = EstMdl11.MA{1};
    
    [EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Asset_Mgr_Diff(2:i,:),'print',false);
    Database.Asset_Mgr_Diff_Pred(i+1,:) = forecast(EstMdl11,1,'Y0',Database.Asset_Mgr_Diff(2:i,:));
    
    [EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Lev_Money_Diff(2:i,:),'print',false);
    Database.Lev_Money_Diff_Pred(i+1,:) = forecast(EstMdl11,1,'Y0',Database.Lev_Money_Diff(2:i,:));
    
    [EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Dealer_Diff(2:i,:),'print',false);
    Database.Dealer_Diff_Pred(i+1,:) = forecast(EstMdl11,1,'Y0',Database.Dealer_Diff(2:i,:));
    
    fprintf('Pred. Left: %d\n', (size(Database,1)-1)-i);
end





