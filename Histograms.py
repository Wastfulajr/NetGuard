import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#drop inf/nan
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)  
#Make a dict for all Attack types
df_dict = {name: group for name, group in df.groupby(' Label') if name != 'BENIGN'}
#use numeric only
numeric_cols = df.select_dtypes(include='number').columns

for col in numeric_cols:
    plt.figure()
    plt.figure(figsize=(20, 6))
    data = [group[col].dropna() for group in df_dict.values()]
    plt.hist(data, bins=30, label=df_dict.keys(), alpha=0.7, rwidth=1.0)
    plt.title(f'Histograms for {col}')
    plt.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))   
    plt.show()   
