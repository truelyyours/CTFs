import pandas as pd
import matplotlib.pyplot as plt

# Load subset for initial analysis
df = pd.read_csv("traces.csv")

# Single trace visualization
plt.figure(figsize=(15,4))
plt.plot(df.iloc[0,:])  # First trace
plt.title("Power Trace Example")
# plt.xlabel("Time samples")
plt.ylabel("Power consumption (W)")
plt.show()
