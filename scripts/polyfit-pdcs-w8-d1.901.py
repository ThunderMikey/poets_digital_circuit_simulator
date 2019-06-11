import numpy as np
import pandas as pd

pdcs_data = pd.read_csv("./docs/data/perf/poets-w8-d1.901.csv", sep=', ')

print(pdcs_data)
y = pdcs_data["app_time"]
x = pdcs_data['depth']

print(x, y)
print(
        np.polyfit(
            x.values.flatten(),
            y.values.flatten(),
            deg=1,
            full=False,
            cov=True)
    )
