import pandas as pd
from sklearn.tree import DecisionTreeRegressor


commodity_dict = {
    "arhar": "static/Arhar.csv",
    "cotton": "static/Cotton.csv",
    "gram": "static/Gram.csv",
    "masoor": "static/Masoor.csv",
    "moong": "static/Moong.csv",
    "sugarcane": "static/Sugarcane.csv",
    "sunflower": "static/Sunflower.csv",
    "wheat": "static/Wheat.csv"
}

for key,values in commodity_dict.items(): 
    data=pd.load_csc(values)
    x=data.iloc[:, :-1].values
    y=data.iloc[:, 3].values
    regressor = DecisionTreeRegressor(max_depth=5)
    regressor.fit(x,y)
    
    
    
    

