import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
df = pd.read_csv('can_data.csv')

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("#", "")
    .str.replace("@", "")
    .str.replace("/", "_")
)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s") # Convert timestamp
df = df.dropna(axis=1, how="all") # Drop empty columns
df = df.dropna(subset=["RPM"]) # Drop rows without RPM
df = df[df["TPS"] <= 100] # TPS should be 0-100%
df = df[df["TPS"] >= 0] # TPS should be positive

# Statistics
avg_rpm = df['RPM'].mean()
max_rpm = df['RPM'].max()
min_rpm = df['RPM'].min()
avg_tps = df['TPS'].mean()
correlation = df['RPM'].corr(df['TPS'])

# RPM categories
low_rpm = len(df[df['RPM'] < 2000])
medium_rpm = len(df[(df['RPM'] >= 2000) & (df['RPM'] < 4000)])
high_rpm = len(df[df['RPM'] >= 4000])

print(f"Average RPM: {avg_rpm:.0f}")
print(f"Max RPM: {max_rpm:.0f}")
print(f"Min RPM: {min_rpm:.0f}")
print(f"Average throttle position: {avg_tps:.1f}%")
print(f"RPM vs Throttle correlation: {correlation:.2f}")
print(f"")
print(f"Low RPM (<2000): {low_rpm} readings ({(low_rpm/len(df)*100):.1f}%)")
print(f"Medium RPM (2000-4000): {medium_rpm} readings ({(medium_rpm/len(df)*100):.1f}%)")
print(f"High RPM (>4000): {high_rpm} readings ({(high_rpm/len(df)*100):.1f}%)")

# Line chart
plt.figure(figsize=(12, 5))
plt.plot(df["timestamp"], df["RPM"], linewidth=1, color='blue')
plt.title("Engine RPM Over Time")
plt.xlabel("Time")
plt.ylabel("RPM")
plt.grid(True, alpha=0.3)
plt.axhline(y=avg_rpm, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg_rpm:.0f} RPM')
plt.legend()
plt.tight_layout()
plt.savefig("rpm_over_time.png")
plt.show()

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df["TPS"], df["RPM"], alpha=0.5, s=10, c='darkgreen')
plt.title("RPM vs Throttle Position")
plt.xlabel("Throttle Position (%)")
plt.ylabel("RPM")
plt.grid(True, alpha=0.3)

if len(df) > 1:
    z = np.polyfit(df["TPS"].dropna(), df["RPM"].dropna(), 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df["TPS"].min(), df["TPS"].max(), 100)
    plt.plot(x_trend, p(x_trend), "r--", alpha=0.8, label=f'Correlation: {correlation:.2f}')
    plt.legend()

plt.tight_layout()
plt.savefig("rpm_vs_tps.png")
plt.show()

# Histogram 
plt.figure(figsize=(10, 5))
plt.hist(df["RPM"].dropna(), bins=40, edgecolor='black', alpha=0.7, color='orange')
plt.title("RPM Distribution")
plt.xlabel("RPM")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3, axis='y')
plt.axvline(x=avg_rpm, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_rpm:.0f}')
plt.legend()
plt.tight_layout()
plt.savefig("rpm_distribution.png")
plt.show()