import numpy as np
from  sklearn.linear_model import LinearRegression
def LinearModel(x,y, xlabel = "S_wa", ylabel = "R_st"):
    x = np.array(x).reshape(-1,1)
    y = np.array(y)
    model = LinearRegression()

    model.fit(x,y)
    Text = f"r2: {'%.3f'%(model.score(x,y))}. {ylabel} = {'%.3f'%(model.coef_[0])}*{xlabel} + {'%.3f'%(model.intercept_)}"
    info = {
        "Text": Text,
        "R2": model.score(x,y),
        "Coef": model.coef_,
        "Intercept": model.intercept_
    }
    return info
