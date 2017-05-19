function [VarName1,Market_and_Exchange_Names,As_of_Date_In_Form_YYMMDD,Report_Date_as_MM_DD_YYYY,CFTC_Contract_Market_Code,CFTC_Market_Code,CFTC_Region_Code,CFTC_Commodity_Code,Open_Interest_All,Dealer_Positions_Long_All,Dealer_Positions_Short_All,Dealer_Positions_Spread_All,Asset_Mgr_Positions_Long_All,Asset_Mgr_Positions_Short_All,Asset_Mgr_Positions_Spread_All,Lev_Money_Positions_Long_All,Lev_Money_Positions_Short_All,Lev_Money_Positions_Spread_All,Other_Rept_Positions_Long_All,Other_Rept_Positions_Short_All,Other_Rept_Positions_Spread_All,Tot_Rept_Positions_Long_All,Tot_Rept_Positions_Short_All,NonRept_Positions_Long_All,NonRept_Positions_Short_All,Change_in_Open_Interest_All,Change_in_Dealer_Long_All,Change_in_Dealer_Short_All,Change_in_Dealer_Spread_All,Change_in_Asset_Mgr_Long_All,Change_in_Asset_Mgr_Short_All,Change_in_Asset_Mgr_Spread_All,Change_in_Lev_Money_Long_All,Change_in_Lev_Money_Short_All,Change_in_Lev_Money_Spread_All,Change_in_Other_Rept_Long_All,Change_in_Other_Rept_Short_All,Change_in_Other_Rept_Spread_All,Change_in_Tot_Rept_Long_All,Change_in_Tot_Rept_Short_All,Change_in_NonRept_Long_All,Change_in_NonRept_Short_All,Pct_of_Open_Interest_All,Pct_of_OI_Dealer_Long_All,Pct_of_OI_Dealer_Short_All,Pct_of_OI_Dealer_Spread_All,Pct_of_OI_Asset_Mgr_Long_All,Pct_of_OI_Asset_Mgr_Short_All,Pct_of_OI_Asset_Mgr_Spread_All,Pct_of_OI_Lev_Money_Long_All,Pct_of_OI_Lev_Money_Short_All,Pct_of_OI_Lev_Money_Spread_All,Pct_of_OI_Other_Rept_Long_All,Pct_of_OI_Other_Rept_Short_All,Pct_of_OI_Other_Rept_Spread_All,Pct_of_OI_Tot_Rept_Long_All,Pct_of_OI_Tot_Rept_Short_All,Pct_of_OI_NonRept_Long_All,Pct_of_OI_NonRept_Short_All,Traders_Tot_All,Traders_Dealer_Long_All,Traders_Dealer_Short_All,Traders_Dealer_Spread_All,Traders_Asset_Mgr_Long_All,Traders_Asset_Mgr_Short_All,Traders_Asset_Mgr_Spread_All,Traders_Lev_Money_Long_All,Traders_Lev_Money_Short_All,Traders_Lev_Money_Spread_All,Traders_Other_Rept_Long_All,Traders_Other_Rept_Short_All,Traders_Other_Rept_Spread_All,Traders_Tot_Rept_Long_All,Traders_Tot_Rept_Short_All,Conc_Gross_LE_4_TDR_Long_All,Conc_Gross_LE_4_TDR_Short_All,Conc_Gross_LE_8_TDR_Long_All,Conc_Gross_LE_8_TDR_Short_All,Conc_Net_LE_4_TDR_Long_All,Conc_Net_LE_4_TDR_Short_All,Conc_Net_LE_8_TDR_Long_All,Conc_Net_LE_8_TDR_Short_All,Contract_Units,CFTC_SubGroup_Code,FutOnly_or_Combined,Leverage_Money_Diff,Leverage_Money_Signal1,Dealer_Diff,Dealer_Signal1,Asset_Mgr_Diff,Asset_Mgr_Signal1] = ImportDataFunction(filename, startRow, endRow)
%IMPORTFILE Import numeric data from a text file as column vectors.
%   [VARNAME1,MARKET_AND_EXCHANGE_NAMES,AS_OF_DATE_IN_FORM_YYMMDD,REPORT_DATE_AS_MM_DD_YYYY,CFTC_CONTRACT_MARKET_CODE,CFTC_MARKET_CODE,CFTC_REGION_CODE,CFTC_COMMODITY_CODE,OPEN_INTEREST_ALL,DEALER_POSITIONS_LONG_ALL,DEALER_POSITIONS_SHORT_ALL,DEALER_POSITIONS_SPREAD_ALL,ASSET_MGR_POSITIONS_LONG_ALL,ASSET_MGR_POSITIONS_SHORT_ALL,ASSET_MGR_POSITIONS_SPREAD_ALL,LEV_MONEY_POSITIONS_LONG_ALL,LEV_MONEY_POSITIONS_SHORT_ALL,LEV_MONEY_POSITIONS_SPREAD_ALL,OTHER_REPT_POSITIONS_LONG_ALL,OTHER_REPT_POSITIONS_SHORT_ALL,OTHER_REPT_POSITIONS_SPREAD_ALL,TOT_REPT_POSITIONS_LONG_ALL,TOT_REPT_POSITIONS_SHORT_ALL,NONREPT_POSITIONS_LONG_ALL,NONREPT_POSITIONS_SHORT_ALL,CHANGE_IN_OPEN_INTEREST_ALL,CHANGE_IN_DEALER_LONG_ALL,CHANGE_IN_DEALER_SHORT_ALL,CHANGE_IN_DEALER_SPREAD_ALL,CHANGE_IN_ASSET_MGR_LONG_ALL,CHANGE_IN_ASSET_MGR_SHORT_ALL,CHANGE_IN_ASSET_MGR_SPREAD_ALL,CHANGE_IN_LEV_MONEY_LONG_ALL,CHANGE_IN_LEV_MONEY_SHORT_ALL,CHANGE_IN_LEV_MONEY_SPREAD_ALL,CHANGE_IN_OTHER_REPT_LONG_ALL,CHANGE_IN_OTHER_REPT_SHORT_ALL,CHANGE_IN_OTHER_REPT_SPREAD_ALL,CHANGE_IN_TOT_REPT_LONG_ALL,CHANGE_IN_TOT_REPT_SHORT_ALL,CHANGE_IN_NONREPT_LONG_ALL,CHANGE_IN_NONREPT_SHORT_ALL,PCT_OF_OPEN_INTEREST_ALL,PCT_OF_OI_DEALER_LONG_ALL,PCT_OF_OI_DEALER_SHORT_ALL,PCT_OF_OI_DEALER_SPREAD_ALL,PCT_OF_OI_ASSET_MGR_LONG_ALL,PCT_OF_OI_ASSET_MGR_SHORT_ALL,PCT_OF_OI_ASSET_MGR_SPREAD_ALL,PCT_OF_OI_LEV_MONEY_LONG_ALL,PCT_OF_OI_LEV_MONEY_SHORT_ALL,PCT_OF_OI_LEV_MONEY_SPREAD_ALL,PCT_OF_OI_OTHER_REPT_LONG_ALL,PCT_OF_OI_OTHER_REPT_SHORT_ALL,PCT_OF_OI_OTHER_REPT_SPREAD_ALL,PCT_OF_OI_TOT_REPT_LONG_ALL,PCT_OF_OI_TOT_REPT_SHORT_ALL,PCT_OF_OI_NONREPT_LONG_ALL,PCT_OF_OI_NONREPT_SHORT_ALL,TRADERS_TOT_ALL,TRADERS_DEALER_LONG_ALL,TRADERS_DEALER_SHORT_ALL,TRADERS_DEALER_SPREAD_ALL,TRADERS_ASSET_MGR_LONG_ALL,TRADERS_ASSET_MGR_SHORT_ALL,TRADERS_ASSET_MGR_SPREAD_ALL,TRADERS_LEV_MONEY_LONG_ALL,TRADERS_LEV_MONEY_SHORT_ALL,TRADERS_LEV_MONEY_SPREAD_ALL,TRADERS_OTHER_REPT_LONG_ALL,TRADERS_OTHER_REPT_SHORT_ALL,TRADERS_OTHER_REPT_SPREAD_ALL,TRADERS_TOT_REPT_LONG_ALL,TRADERS_TOT_REPT_SHORT_ALL,CONC_GROSS_LE_4_TDR_LONG_ALL,CONC_GROSS_LE_4_TDR_SHORT_ALL,CONC_GROSS_LE_8_TDR_LONG_ALL,CONC_GROSS_LE_8_TDR_SHORT_ALL,CONC_NET_LE_4_TDR_LONG_ALL,CONC_NET_LE_4_TDR_SHORT_ALL,CONC_NET_LE_8_TDR_LONG_ALL,CONC_NET_LE_8_TDR_SHORT_ALL,CONTRACT_UNITS,CFTC_SUBGROUP_CODE,FUTONLY_OR_COMBINED,LEVERAGE_MONEY_DIFF,LEVERAGE_MONEY_SIGNAL1,DEALER_DIFF,DEALER_SIGNAL1,ASSET_MGR_DIFF,ASSET_MGR_SIGNAL1]
%   = IMPORTFILE(FILENAME) Reads data from text file FILENAME for the
%   default selection.
%
%   [VARNAME1,MARKET_AND_EXCHANGE_NAMES,AS_OF_DATE_IN_FORM_YYMMDD,REPORT_DATE_AS_MM_DD_YYYY,CFTC_CONTRACT_MARKET_CODE,CFTC_MARKET_CODE,CFTC_REGION_CODE,CFTC_COMMODITY_CODE,OPEN_INTEREST_ALL,DEALER_POSITIONS_LONG_ALL,DEALER_POSITIONS_SHORT_ALL,DEALER_POSITIONS_SPREAD_ALL,ASSET_MGR_POSITIONS_LONG_ALL,ASSET_MGR_POSITIONS_SHORT_ALL,ASSET_MGR_POSITIONS_SPREAD_ALL,LEV_MONEY_POSITIONS_LONG_ALL,LEV_MONEY_POSITIONS_SHORT_ALL,LEV_MONEY_POSITIONS_SPREAD_ALL,OTHER_REPT_POSITIONS_LONG_ALL,OTHER_REPT_POSITIONS_SHORT_ALL,OTHER_REPT_POSITIONS_SPREAD_ALL,TOT_REPT_POSITIONS_LONG_ALL,TOT_REPT_POSITIONS_SHORT_ALL,NONREPT_POSITIONS_LONG_ALL,NONREPT_POSITIONS_SHORT_ALL,CHANGE_IN_OPEN_INTEREST_ALL,CHANGE_IN_DEALER_LONG_ALL,CHANGE_IN_DEALER_SHORT_ALL,CHANGE_IN_DEALER_SPREAD_ALL,CHANGE_IN_ASSET_MGR_LONG_ALL,CHANGE_IN_ASSET_MGR_SHORT_ALL,CHANGE_IN_ASSET_MGR_SPREAD_ALL,CHANGE_IN_LEV_MONEY_LONG_ALL,CHANGE_IN_LEV_MONEY_SHORT_ALL,CHANGE_IN_LEV_MONEY_SPREAD_ALL,CHANGE_IN_OTHER_REPT_LONG_ALL,CHANGE_IN_OTHER_REPT_SHORT_ALL,CHANGE_IN_OTHER_REPT_SPREAD_ALL,CHANGE_IN_TOT_REPT_LONG_ALL,CHANGE_IN_TOT_REPT_SHORT_ALL,CHANGE_IN_NONREPT_LONG_ALL,CHANGE_IN_NONREPT_SHORT_ALL,PCT_OF_OPEN_INTEREST_ALL,PCT_OF_OI_DEALER_LONG_ALL,PCT_OF_OI_DEALER_SHORT_ALL,PCT_OF_OI_DEALER_SPREAD_ALL,PCT_OF_OI_ASSET_MGR_LONG_ALL,PCT_OF_OI_ASSET_MGR_SHORT_ALL,PCT_OF_OI_ASSET_MGR_SPREAD_ALL,PCT_OF_OI_LEV_MONEY_LONG_ALL,PCT_OF_OI_LEV_MONEY_SHORT_ALL,PCT_OF_OI_LEV_MONEY_SPREAD_ALL,PCT_OF_OI_OTHER_REPT_LONG_ALL,PCT_OF_OI_OTHER_REPT_SHORT_ALL,PCT_OF_OI_OTHER_REPT_SPREAD_ALL,PCT_OF_OI_TOT_REPT_LONG_ALL,PCT_OF_OI_TOT_REPT_SHORT_ALL,PCT_OF_OI_NONREPT_LONG_ALL,PCT_OF_OI_NONREPT_SHORT_ALL,TRADERS_TOT_ALL,TRADERS_DEALER_LONG_ALL,TRADERS_DEALER_SHORT_ALL,TRADERS_DEALER_SPREAD_ALL,TRADERS_ASSET_MGR_LONG_ALL,TRADERS_ASSET_MGR_SHORT_ALL,TRADERS_ASSET_MGR_SPREAD_ALL,TRADERS_LEV_MONEY_LONG_ALL,TRADERS_LEV_MONEY_SHORT_ALL,TRADERS_LEV_MONEY_SPREAD_ALL,TRADERS_OTHER_REPT_LONG_ALL,TRADERS_OTHER_REPT_SHORT_ALL,TRADERS_OTHER_REPT_SPREAD_ALL,TRADERS_TOT_REPT_LONG_ALL,TRADERS_TOT_REPT_SHORT_ALL,CONC_GROSS_LE_4_TDR_LONG_ALL,CONC_GROSS_LE_4_TDR_SHORT_ALL,CONC_GROSS_LE_8_TDR_LONG_ALL,CONC_GROSS_LE_8_TDR_SHORT_ALL,CONC_NET_LE_4_TDR_LONG_ALL,CONC_NET_LE_4_TDR_SHORT_ALL,CONC_NET_LE_8_TDR_LONG_ALL,CONC_NET_LE_8_TDR_SHORT_ALL,CONTRACT_UNITS,CFTC_SUBGROUP_CODE,FUTONLY_OR_COMBINED,LEVERAGE_MONEY_DIFF,LEVERAGE_MONEY_SIGNAL1,DEALER_DIFF,DEALER_SIGNAL1,ASSET_MGR_DIFF,ASSET_MGR_SIGNAL1]
%   = IMPORTFILE(FILENAME, STARTROW, ENDROW) Reads data from rows STARTROW
%   through ENDROW of text file FILENAME.
%
% Example:
%   [VarName1,Market_and_Exchange_Names,As_of_Date_In_Form_YYMMDD,Report_Date_as_MM_DD_YYYY,CFTC_Contract_Market_Code,CFTC_Market_Code,CFTC_Region_Code,CFTC_Commodity_Code,Open_Interest_All,Dealer_Positions_Long_All,Dealer_Positions_Short_All,Dealer_Positions_Spread_All,Asset_Mgr_Positions_Long_All,Asset_Mgr_Positions_Short_All,Asset_Mgr_Positions_Spread_All,Lev_Money_Positions_Long_All,Lev_Money_Positions_Short_All,Lev_Money_Positions_Spread_All,Other_Rept_Positions_Long_All,Other_Rept_Positions_Short_All,Other_Rept_Positions_Spread_All,Tot_Rept_Positions_Long_All,Tot_Rept_Positions_Short_All,NonRept_Positions_Long_All,NonRept_Positions_Short_All,Change_in_Open_Interest_All,Change_in_Dealer_Long_All,Change_in_Dealer_Short_All,Change_in_Dealer_Spread_All,Change_in_Asset_Mgr_Long_All,Change_in_Asset_Mgr_Short_All,Change_in_Asset_Mgr_Spread_All,Change_in_Lev_Money_Long_All,Change_in_Lev_Money_Short_All,Change_in_Lev_Money_Spread_All,Change_in_Other_Rept_Long_All,Change_in_Other_Rept_Short_All,Change_in_Other_Rept_Spread_All,Change_in_Tot_Rept_Long_All,Change_in_Tot_Rept_Short_All,Change_in_NonRept_Long_All,Change_in_NonRept_Short_All,Pct_of_Open_Interest_All,Pct_of_OI_Dealer_Long_All,Pct_of_OI_Dealer_Short_All,Pct_of_OI_Dealer_Spread_All,Pct_of_OI_Asset_Mgr_Long_All,Pct_of_OI_Asset_Mgr_Short_All,Pct_of_OI_Asset_Mgr_Spread_All,Pct_of_OI_Lev_Money_Long_All,Pct_of_OI_Lev_Money_Short_All,Pct_of_OI_Lev_Money_Spread_All,Pct_of_OI_Other_Rept_Long_All,Pct_of_OI_Other_Rept_Short_All,Pct_of_OI_Other_Rept_Spread_All,Pct_of_OI_Tot_Rept_Long_All,Pct_of_OI_Tot_Rept_Short_All,Pct_of_OI_NonRept_Long_All,Pct_of_OI_NonRept_Short_All,Traders_Tot_All,Traders_Dealer_Long_All,Traders_Dealer_Short_All,Traders_Dealer_Spread_All,Traders_Asset_Mgr_Long_All,Traders_Asset_Mgr_Short_All,Traders_Asset_Mgr_Spread_All,Traders_Lev_Money_Long_All,Traders_Lev_Money_Short_All,Traders_Lev_Money_Spread_All,Traders_Other_Rept_Long_All,Traders_Other_Rept_Short_All,Traders_Other_Rept_Spread_All,Traders_Tot_Rept_Long_All,Traders_Tot_Rept_Short_All,Conc_Gross_LE_4_TDR_Long_All,Conc_Gross_LE_4_TDR_Short_All,Conc_Gross_LE_8_TDR_Long_All,Conc_Gross_LE_8_TDR_Short_All,Conc_Net_LE_4_TDR_Long_All,Conc_Net_LE_4_TDR_Short_All,Conc_Net_LE_8_TDR_Long_All,Conc_Net_LE_8_TDR_Short_All,Contract_Units,CFTC_SubGroup_Code,FutOnly_or_Combined,Leverage_Money_Diff,Leverage_Money_Signal1,Dealer_Diff,Dealer_Signal1,Asset_Mgr_Diff,Asset_Mgr_Signal1] = importfile('JAPANESE YEN.csv',2, 552);
%
%    See also TEXTSCAN.

% Auto-generated by MATLAB on 2017/02/06 20:24:18

%% Initialize variables.
delimiter = ',';
if nargin<=2
    startRow = 2;
    endRow = inf;
end

%% Read columns of data as text:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(1)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(block)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
    for col=1:length(dataArray)
        dataArray{col} = [dataArray{col};dataArrayBlock{col}];
    end
end

%% Close the text file.
fclose(fileID);

%% Convert the contents of columns containing numeric text to numbers.
% Replace non-numeric text with NaN.
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = dataArray{col};
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));

for col=[1,3,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,84,86,88,90]
    % Converts text in the input cell array to numbers. Replaced non-numeric
    % text with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1);
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData{row}, regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if any(numbers==',');
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(numbers, thousandsRegExp, 'once'));
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric text to numbers.
            if ~invalidThousandsSeparator;
                numbers = textscan(strrep(numbers, ',', ''), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch me
        end
    end
end


%% Split data into numeric and cell columns.
rawNumericColumns = raw(:, [1,3,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,84,86,88,90]);
rawCellColumns = raw(:, [2,4,6,83,85,87,89,91]);


%% Replace blank cells with 0.0
R = cellfun(@(x) isempty(x) || (ischar(x) && all(x==' ')),rawNumericColumns);
rawNumericColumns(R) = {0.0}; % Replace blank cells

%% Allocate imported array to column variable names
VarName1 = cell2mat(rawNumericColumns(:, 1));
Market_and_Exchange_Names = rawCellColumns(:, 1);
As_of_Date_In_Form_YYMMDD = cell2mat(rawNumericColumns(:, 2));
Report_Date_as_MM_DD_YYYY = rawCellColumns(:, 2);
CFTC_Contract_Market_Code = cell2mat(rawNumericColumns(:, 3));
CFTC_Market_Code = rawCellColumns(:, 3);
CFTC_Region_Code = cell2mat(rawNumericColumns(:, 4));
CFTC_Commodity_Code = cell2mat(rawNumericColumns(:, 5));
Open_Interest_All = cell2mat(rawNumericColumns(:, 6));
Dealer_Positions_Long_All = cell2mat(rawNumericColumns(:, 7));
Dealer_Positions_Short_All = cell2mat(rawNumericColumns(:, 8));
Dealer_Positions_Spread_All = cell2mat(rawNumericColumns(:, 9));
Asset_Mgr_Positions_Long_All = cell2mat(rawNumericColumns(:, 10));
Asset_Mgr_Positions_Short_All = cell2mat(rawNumericColumns(:, 11));
Asset_Mgr_Positions_Spread_All = cell2mat(rawNumericColumns(:, 12));
Lev_Money_Positions_Long_All = cell2mat(rawNumericColumns(:, 13));
Lev_Money_Positions_Short_All = cell2mat(rawNumericColumns(:, 14));
Lev_Money_Positions_Spread_All = cell2mat(rawNumericColumns(:, 15));
Other_Rept_Positions_Long_All = cell2mat(rawNumericColumns(:, 16));
Other_Rept_Positions_Short_All = cell2mat(rawNumericColumns(:, 17));
Other_Rept_Positions_Spread_All = cell2mat(rawNumericColumns(:, 18));
Tot_Rept_Positions_Long_All = cell2mat(rawNumericColumns(:, 19));
Tot_Rept_Positions_Short_All = cell2mat(rawNumericColumns(:, 20));
NonRept_Positions_Long_All = cell2mat(rawNumericColumns(:, 21));
NonRept_Positions_Short_All = cell2mat(rawNumericColumns(:, 22));
Change_in_Open_Interest_All = cell2mat(rawNumericColumns(:, 23));
Change_in_Dealer_Long_All = cell2mat(rawNumericColumns(:, 24));
Change_in_Dealer_Short_All = cell2mat(rawNumericColumns(:, 25));
Change_in_Dealer_Spread_All = cell2mat(rawNumericColumns(:, 26));
Change_in_Asset_Mgr_Long_All = cell2mat(rawNumericColumns(:, 27));
Change_in_Asset_Mgr_Short_All = cell2mat(rawNumericColumns(:, 28));
Change_in_Asset_Mgr_Spread_All = cell2mat(rawNumericColumns(:, 29));
Change_in_Lev_Money_Long_All = cell2mat(rawNumericColumns(:, 30));
Change_in_Lev_Money_Short_All = cell2mat(rawNumericColumns(:, 31));
Change_in_Lev_Money_Spread_All = cell2mat(rawNumericColumns(:, 32));
Change_in_Other_Rept_Long_All = cell2mat(rawNumericColumns(:, 33));
Change_in_Other_Rept_Short_All = cell2mat(rawNumericColumns(:, 34));
Change_in_Other_Rept_Spread_All = cell2mat(rawNumericColumns(:, 35));
Change_in_Tot_Rept_Long_All = cell2mat(rawNumericColumns(:, 36));
Change_in_Tot_Rept_Short_All = cell2mat(rawNumericColumns(:, 37));
Change_in_NonRept_Long_All = cell2mat(rawNumericColumns(:, 38));
Change_in_NonRept_Short_All = cell2mat(rawNumericColumns(:, 39));
Pct_of_Open_Interest_All = cell2mat(rawNumericColumns(:, 40));
Pct_of_OI_Dealer_Long_All = cell2mat(rawNumericColumns(:, 41));
Pct_of_OI_Dealer_Short_All = cell2mat(rawNumericColumns(:, 42));
Pct_of_OI_Dealer_Spread_All = cell2mat(rawNumericColumns(:, 43));
Pct_of_OI_Asset_Mgr_Long_All = cell2mat(rawNumericColumns(:, 44));
Pct_of_OI_Asset_Mgr_Short_All = cell2mat(rawNumericColumns(:, 45));
Pct_of_OI_Asset_Mgr_Spread_All = cell2mat(rawNumericColumns(:, 46));
Pct_of_OI_Lev_Money_Long_All = cell2mat(rawNumericColumns(:, 47));
Pct_of_OI_Lev_Money_Short_All = cell2mat(rawNumericColumns(:, 48));
Pct_of_OI_Lev_Money_Spread_All = cell2mat(rawNumericColumns(:, 49));
Pct_of_OI_Other_Rept_Long_All = cell2mat(rawNumericColumns(:, 50));
Pct_of_OI_Other_Rept_Short_All = cell2mat(rawNumericColumns(:, 51));
Pct_of_OI_Other_Rept_Spread_All = cell2mat(rawNumericColumns(:, 52));
Pct_of_OI_Tot_Rept_Long_All = cell2mat(rawNumericColumns(:, 53));
Pct_of_OI_Tot_Rept_Short_All = cell2mat(rawNumericColumns(:, 54));
Pct_of_OI_NonRept_Long_All = cell2mat(rawNumericColumns(:, 55));
Pct_of_OI_NonRept_Short_All = cell2mat(rawNumericColumns(:, 56));
Traders_Tot_All = cell2mat(rawNumericColumns(:, 57));
Traders_Dealer_Long_All = cell2mat(rawNumericColumns(:, 58));
Traders_Dealer_Short_All = cell2mat(rawNumericColumns(:, 59));
Traders_Dealer_Spread_All = cell2mat(rawNumericColumns(:, 60));
Traders_Asset_Mgr_Long_All = cell2mat(rawNumericColumns(:, 61));
Traders_Asset_Mgr_Short_All = cell2mat(rawNumericColumns(:, 62));
Traders_Asset_Mgr_Spread_All = cell2mat(rawNumericColumns(:, 63));
Traders_Lev_Money_Long_All = cell2mat(rawNumericColumns(:, 64));
Traders_Lev_Money_Short_All = cell2mat(rawNumericColumns(:, 65));
Traders_Lev_Money_Spread_All = cell2mat(rawNumericColumns(:, 66));
Traders_Other_Rept_Long_All = cell2mat(rawNumericColumns(:, 67));
Traders_Other_Rept_Short_All = cell2mat(rawNumericColumns(:, 68));
Traders_Other_Rept_Spread_All = cell2mat(rawNumericColumns(:, 69));
Traders_Tot_Rept_Long_All = cell2mat(rawNumericColumns(:, 70));
Traders_Tot_Rept_Short_All = cell2mat(rawNumericColumns(:, 71));
Conc_Gross_LE_4_TDR_Long_All = cell2mat(rawNumericColumns(:, 72));
Conc_Gross_LE_4_TDR_Short_All = cell2mat(rawNumericColumns(:, 73));
Conc_Gross_LE_8_TDR_Long_All = cell2mat(rawNumericColumns(:, 74));
Conc_Gross_LE_8_TDR_Short_All = cell2mat(rawNumericColumns(:, 75));
Conc_Net_LE_4_TDR_Long_All = cell2mat(rawNumericColumns(:, 76));
Conc_Net_LE_4_TDR_Short_All = cell2mat(rawNumericColumns(:, 77));
Conc_Net_LE_8_TDR_Long_All = cell2mat(rawNumericColumns(:, 78));
Conc_Net_LE_8_TDR_Short_All = cell2mat(rawNumericColumns(:, 79));
Contract_Units = rawCellColumns(:, 4);
CFTC_SubGroup_Code = cell2mat(rawNumericColumns(:, 80));
FutOnly_or_Combined = rawCellColumns(:, 5);
Leverage_Money_Diff = cell2mat(rawNumericColumns(:, 81));
Leverage_Money_Signal1 = rawCellColumns(:, 6);
Dealer_Diff = cell2mat(rawNumericColumns(:, 82));
Dealer_Signal1 = rawCellColumns(:, 7);
Asset_Mgr_Diff = cell2mat(rawNumericColumns(:, 83));
Asset_Mgr_Signal1 = rawCellColumns(:, 8);


