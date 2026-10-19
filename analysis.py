import pandas as pd
import matplotlib.pyplot as plt

# Load the synthetic sample data
df = pd.read_csv("shipments.csv", parse_dates=["Ship_Date"])

# Basic data checks
print("Rows:", len(df))
print("Missing values by column:")
print(df.isna().sum())

# Key performance indicators
total_shipments = len(df)
total_cost = df["Shipping_Cost_USD"].sum()
avg_cost = df["Shipping_Cost_USD"].mean()
on_time_rate = df["On_Time"].eq("Yes").mean() * 100
avg_transit = df["Actual_Transit_Days"].mean()

print("\nKEY PERFORMANCE INDICATORS")
print(f"Total shipments: {total_shipments:,}")
print(f"Total shipping cost: ${total_cost:,.2f}")
print(f"Average cost per shipment: ${avg_cost:,.2f}")
print(f"On-time delivery rate: {on_time_rate:.1f}%")
print(f"Average actual transit time: {avg_transit:.2f} days")

# Carrier comparison
carrier_summary = (
    df.groupby("Carrier")
      .agg(
          Shipments=("Shipment_ID", "count"),
          Total_Cost=("Shipping_Cost_USD", "sum"),
          Average_Cost=("Shipping_Cost_USD", "mean"),
          On_Time_Rate=("On_Time", lambda s: s.eq("Yes").mean() * 100),
      )
      .sort_values("Average_Cost", ascending=False)
)
print("\nCARRIER SUMMARY")
print(carrier_summary.round(2))

# Regional transit time comparison
region_summary = (
    df.groupby("Region")
      .agg(
          Shipments=("Shipment_ID", "count"),
          Average_Transit_Days=("Actual_Transit_Days", "mean"),
          On_Time_Rate=("On_Time", lambda s: s.eq("Yes").mean() * 100),
      )
      .sort_values("Average_Transit_Days", ascending=False)
)
print("\nREGION SUMMARY")
print(region_summary.round(2))

# Chart 1: average shipping cost by carrier
carrier_summary["Average_Cost"].sort_values().plot(kind="barh")
plt.title("Average Shipping Cost by Carrier")
plt.xlabel("Average shipping cost (USD)")
plt.ylabel("Carrier")
plt.tight_layout()
plt.show()

# Chart 2: on-time delivery rate by region
region_summary["On_Time_Rate"].sort_values().plot(kind="barh")
plt.title("On-Time Delivery Rate by Region")
plt.xlabel("On-time delivery (%)")
plt.ylabel("Region")
plt.xlim(0, 100)
plt.tight_layout()
plt.show()

# Chart 3: shipment volume by mode
df["Mode"].value_counts().plot(kind="bar")
plt.title("Shipment Count by Mode")
plt.xlabel("Mode")
plt.ylabel("Number of shipments")
plt.tight_layout()
plt.show()
