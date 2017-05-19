 function [bestAIC,bestBIC]=select_model(y,ARmax,MAmax,Pmax,Qmax)
bestAIC=[0 0 0 0];
bestBIC=[0 0 0 0];
for i=0:ARmax
    for j=0:MAmax
        for l=0:Qmax
            if l==0
                Pmaxlimit=0;
            else
                Pmaxlimit=Pmax;
            end
            for k=0:Pmaxlimit

                
                VarMdl = garch(k,l);

                
                Mdl = arima(i,0,j);
                Mdl.Variance = VarMdl;
                [EstMdl, EstParamCov] = ...
                    estimate(Mdl,y, 'Display', 'off');

                
                [~, ~, LLF] = infer(...
                    EstMdl, y);
                NumParams = sum(any(...
                    EstParamCov));
                NumObs=size(y,2);
                [AIC,BIC] = aicbic(LLF,NumParams,NumObs);
                if i==0 && j==0 && k==0 && l==0
                    AICbest=AIC;
                    BICbest=BIC;
                else
                    if AIC<=AICbest
                        AICbest=AIC;
                        bestAIC=[i j k l];
                    end
                    if BIC<=BICbest
                        BICbest=BIC;
                        bestBIC=[i j k l];
                    end
                end
            end
        end
    end
end