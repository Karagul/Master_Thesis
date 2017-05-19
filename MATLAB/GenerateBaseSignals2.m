% Define  File to Load
% WIndows
%Signals_filename = 'C:\Users\Jannis\Dropbox\Master_Thesis\MATLAB\Databases/JAPANESE YEN.csv';
%OptionsDatabase_filename = 'C:\Users\Jannis\Dropbox\Master_Thesis\MATLAB\Databases/OptionsDatabase.csv';
% Mac
Signals_filename = '/Users/MacMini1/Dropbox/Master_Thesis/MATLAB/Databases/EURO FX.csv';
OptionsDatabase_filename = '/Users/MacMini1/Dropbox/Master_Thesis/MATLAB/Databases/OptionsDatabase.csv';

%Parameters
instrument = 'EURUSD';
threshhold = 0.1;

% Select Number of players
p = 3;
Players = {'Dealer','Asset_Mgr','Leverage_Money'};

% Load FIle
Database = ImportDataFunctionTable(Signals_filename, 2, inf );
OptionsDatabase = ImportOptionsDatabase(OptionsDatabase_filename, 2, inf );

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






Database.Asset_Mgr_Diff_Pred = zeros(size(Database,1), 1);
Database.Lev_Money_Diff_Pred = zeros(size(Database,1), 1);
Database.Dealer_Diff_Pred = zeros(size(Database,1), 1);

%Database.AR = zeros(size(Database,1), 1);
%Database.MA = zeros(size(Database,1), 1);



% Create Model


%Residuals = infer(EstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:));
ToEstMdl11 = arima(1,0,1);
[EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:),'print',false);
Asset_Mgr_Est_Data = Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl11,Database.Asset_Mgr_Diff(1:round(size(Database,1)/2),:));

ToEstMdl12 = arima(1,0,1);
[EstMdl12,EstParamCov12,logl12] = estimate(ToEstMdl12,Database.Lev_Money_Diff(1:round(size(Database,1)/2),:),'print',false);
Lev_Money_Est_Data = Database.Lev_Money_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl12,Database.Lev_Money_Diff(1:round(size(Database,1)/2),:));

ToEstMdl13 = arima(1,0,1);
[EstMdl13,EstParamCov13,logl13] = estimate(ToEstMdl13,Database.Dealer_Diff(1:round(size(Database,1)/2),:),'print',false);
Dealer_Est_Data = Database.Dealer_Diff(1:round(size(Database,1)/2),:) - infer(EstMdl13,Database.Dealer_Diff(1:round(size(Database,1)/2),:));

for i = 1:round(size(Database,1)/2)
    Database.Asset_Mgr_Diff_Pred(i,:) = Asset_Mgr_Est_Data(i,:);
    Database.Lev_Money_Diff_Pred(i,:) = Lev_Money_Est_Data(i,:);
    Database.Dealer_Diff_Pred(i,:) = Dealer_Est_Data(i,:);
end


Database.Asset_Mgr_Alpha = zeros(size(Database,1), 1);
Database.Asset_Mgr_Diff_Comb_Pred = zeros(size(Database,1), 1);
Database.Asset_Mgr_PL = zeros(size(Database,1), 1);

Database.Lev_Money_Alpha = zeros(size(Database,1), 1);
Database.Lev_Money_Diff_Comb_Pred = zeros(size(Database,1), 1);
Database.Lev_Money_PL = zeros(size(Database,1), 1);

Database.Dealer_Alpha = zeros(size(Database,1), 1);
Database.Dealer_Diff_Comb_Pred = zeros(size(Database,1), 1);
Database.Dealer_PL = zeros(size(Database,1), 1);

DatabaseColumnsNumber = width(Database);
Database = innerjoin(Database, OptionsDatabase);

cols2remove = double.empty();
for i = DatabaseColumnsNumber+1:width(Database)
   if any(cell2mat(regexp(Database.Properties.VariableNames(i),instrument))) < 1
       cols2remove(end+1) = i;
   end
end
Database(:,cols2remove)=[];


OptimalWeight_Asset_Mgr = 0;
OptimalWeight_Lev_Money = 0;
OptimalWeight_Dealer = 0;
MaximumFinalEquity_Asset_Mgr = 0;
MaximumFinalEquity_Lev_Money = 0;
MaximumFinalEquity_Dealer = 0;
for i = 1:100.0
    Database.Asset_Mgr_Alpha(:,:) = i./100.0;
    Database.Asset_Mgr_Diff_Comb_Pred(:,:) = i./100.0*Database.Asset_Mgr_Diff + (1-i./100.0)*Database.Asset_Mgr_Diff_Pred;
    
    Database.Lev_Money_Alpha(:,:) = i./100.0;
    Database.Lev_Money_Diff_Comb_Pred(:,:) = i./100.0*Database.Lev_Money_Diff + (1-i./100.0)*Database.Lev_Money_Diff_Pred;
    
    Database.Dealer_Alpha(:,:) = i./100.0;
    Database.Dealer_Diff_Comb_Pred(:,:) = i./100.0*Database.Dealer_Diff + (1-i./100.0)*Database.Dealer_Diff_Pred;
    
    
    % Loop through the rows
    for j = 1:round(size(Database,1)/2)+1
        % Determine the Direction of the trade
        if j == 1
            Database.Asset_Mgr_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Asset_Mgr_Diff_Comb_Pred(j,:)>threshhold
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:) + Database{j,width(Database)};
            elseif Database.Asset_Mgr_Diff_Comb_Pred(j,:)<-threshhold
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:) + Database{j,width(Database)-1};
            else
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:);
            end
        end
        
        % Determine the Direction of the trade
        if j == 1
            Database.Lev_Money_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Lev_Money_Diff_Comb_Pred(j,:)>threshhold
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:) + Database{j,width(Database)};
            elseif Database.Lev_Money_Diff_Comb_Pred(j,:)<-threshhold
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:) + Database{j,width(Database)-1};
            else
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:);
            end
        end
        
        % Determine the Direction of the trade
        if j == 1
            Database.Dealer_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Dealer_Diff_Comb_Pred(j,:)>threshhold
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:) + Database{j,width(Database)-1};
            elseif Database.Dealer_Diff_Comb_Pred(j,:)<-threshhold
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:) + Database{j,width(Database)};
            else
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:);
            end
        end
        
    end
    
    
    if Database.Asset_Mgr_PL(round(size(Database,1)/2)+1,:) > MaximumFinalEquity_Asset_Mgr
        MaximumFinalEquity_Asset_Mgr = Database.Asset_Mgr_PL(round(size(Database,1)/2)+1,:);
        OptimalWeight_Asset_Mgr = i./100.0;
    end
        
    if Database.Lev_Money_PL(round(size(Database,1)/2)+1,:) > MaximumFinalEquity_Lev_Money
        MaximumFinalEquity_Lev_Money = Database.Lev_Money_PL(round(size(Database,1)/2)+1,:);
        OptimalWeight_Lev_Money = i./100.0;
    end
    
    if Database.Dealer_PL(round(size(Database,1)/2)+1,:) > MaximumFinalEquity_Dealer
        MaximumFinalEquity_Dealer = Database.Dealer_PL(round(size(Database,1)/2)+1,:);
        OptimalWeight_Dealer = i./100.0;
    end
end




ToEstMdl1_Pred1 = arima(1,0,1);
for i = round(size(Database,1)/2)+1:(size(Database,1)-1)
    %[EstMdl11,EstParamCov11,logl11] = estimate(ToEstMdl11,Database.Asset_Mgr_Ret(2:i,:),'print',false);
    %Database.AR(i,:) = EstMdl11.AR{1};
    %Database.MA(i,:) = EstMdl11.MA{1};
    
    [ToEstMdl1_Pred1,EstParamCov11,logl11] = estimate(ToEstMdl1_Pred1,Database.Asset_Mgr_Diff(2:i,:),'print',false);
    Database.Asset_Mgr_Diff_Pred(i+1,:) = forecast(ToEstMdl1_Pred1,1,'Y0',Database.Asset_Mgr_Diff(2:i,:));
    
    [ToEstMdl1_Pred1,EstParamCov11,logl11] = estimate(ToEstMdl1_Pred1,Database.Lev_Money_Diff(2:i,:),'print',false);
    Database.Lev_Money_Diff_Pred(i+1,:) = forecast(ToEstMdl1_Pred1,1,'Y0',Database.Lev_Money_Diff(2:i,:));
    
    [ToEstMdl1_Pred1,EstParamCov11,logl11] = estimate(ToEstMdl1_Pred1,Database.Dealer_Diff(2:i,:),'print',false);
    Database.Dealer_Diff_Pred(i+1,:) = forecast(ToEstMdl1_Pred1,1,'Y0',Database.Dealer_Diff(2:i,:));
    
    fprintf('Pred. Left: %d\n', (size(Database,1)-1)-i);
end

Database.Asset_Mgr_Alpha(:,:) = OptimalWeight_Asset_Mgr;
Database.Asset_Mgr_Diff_Comb_Pred(:,:) = OptimalWeight_Asset_Mgr*Database.Asset_Mgr_Diff + (1-OptimalWeight_Asset_Mgr)*Database.Asset_Mgr_Diff_Pred;

Database.Lev_Money_Alpha(:,:) = OptimalWeight_Lev_Money;
Database.Lev_Money_Diff_Comb_Pred(:,:) = OptimalWeight_Lev_Money*Database.Lev_Money_Diff + (1-OptimalWeight_Lev_Money)*Database.Lev_Money_Diff_Pred;

Database.Dealer_Alpha(:,:) = OptimalWeight_Dealer;
Database.Dealer_Diff_Comb_Pred(:,:) = OptimalWeight_Dealer*Database.Dealer_Diff + (1-OptimalWeight_Dealer)*Database.Dealer_Diff_Pred;
    
for j = 1:size(Database,1)
     % Determine the Direction of the trade
        if j == 1
            Database.Asset_Mgr_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Asset_Mgr_Diff_Comb_Pred(j,:)>threshhold
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:) + Database{j,width(Database)};
            elseif Database.Asset_Mgr_Diff_Comb_Pred(j,:)<-threshhold
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:) + Database{j,width(Database)-1};
            else
                Database.Asset_Mgr_PL(j,:) = Database.Asset_Mgr_PL(j-1,:);
            end
        end
        
        % Determine the Direction of the trade
        if j == 1
            Database.Lev_Money_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Lev_Money_Diff_Comb_Pred(j,:)>threshhold
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:) + Database{j,width(Database)};
            elseif Database.Lev_Money_Diff_Comb_Pred(j,:)<-threshhold
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:) + Database{j,width(Database)-1};
            else
                Database.Lev_Money_PL(j,:) = Database.Lev_Money_PL(j-1,:);
            end
        end
        
        % Determine the Direction of the trade
        if j == 1
            Database.Dealer_PL(j,:) = Database{j,width(Database)};
        else
            if Database.Dealer_Diff_Comb_Pred(j,:)>threshhold
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:) + Database{j,width(Database)-1};
            elseif Database.Dealer_Diff_Comb_Pred(j,:)<-threshhold
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:) + Database{j,width(Database)};
            else
                Database.Dealer_PL(j,:) = Database.Dealer_PL(j-1,:);
            end
        end
end
