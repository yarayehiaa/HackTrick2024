import pickle
import pandas as pd

with open('C:\\Users\\En.Yara\\Desktop\\HackTrick24\\Solvers\\prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
def results():
    future_dates = pd.date_range(start='2016-11-12', periods=50)
    future = pd.DataFrame({'ds': future_dates})
    forecast = model.predict(future[['ds']])

    
    forecast[['ds', 'yhat']]
    return forecast['yhat'].round().tolist()

x= results()
print(x)
    
    