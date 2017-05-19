# Master_Thesis
Factor models for optimised option trading strategies

The present paper investigates the use of the CFTC positioning information within the
scope of a currency and precious metals option-based investment strategy. In more detail, the
CFTC data provide information on the weekly positioning of diferent market participants in
an array of underlying assets. The predictive power of these fgures through the lens of a raw
model, an AR-based model and a GARCH-based model is investigated, and benchmarked
through an option trading strategy. The strategy therefore consists of selling options, collect-
ing the respective premia, and settling any exercises at expiry one week later. The AR-based
model, a combination of a filter and an optimisation process between the latest positioning
information and an AR(1) forecast, is shown to signifcantly outperform a simple follow-the-
data approach. The GARCH model on the other hand, is proven to accurately forecast high
volatility periods and thus avoid losing trades. Given the diversity of the models generated
and range of assets available, the Limited Asset Markowitz process is called upon to produce
an investable portfolio comprised of five assets. Featuring an annualised return of +3.06%, a
Sharpe Ratio of 1.05 and a Leverage of 1, the resulting portfolio is shown to outperform an
equally weighted benchmark and a raw-based benchmark. Furthermore, its' correlation to a
number of market benchmarks is low; combining this with the mentioned metrics yields an
investment process with attractive risk / reward properties.
