import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#Select only numerics
numeric_cols = df.select_dtypes(include='number').columns

# Filter columns: remove all-NaN, constant, etc
safe_cols = []
for col in numeric_cols:
    series = df[col]
    clean_series = series.replace([np.inf, -np.inf], np.nan).dropna()
    if clean_series.nunique() > 1 and clean_series.size > 0:
        safe_cols.append(col)

per_page = 12
n_pages = math.ceil(len(safe_cols) / per_page)

for i in range(n_pages):
    cols_subset = safe_cols[i * per_page:(i + 1) * per_page]
    df[cols_subset].replace([np.inf, -np.inf], np.nan).dropna().hist(bins=30, figsize=(16, 12), edgecolor='black', layout=(3, 4))
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.suptitle(f'Histograms: Features {i * per_page + 1} to {(i + 1) * per_page}', fontsize=16)
    plt.show()
