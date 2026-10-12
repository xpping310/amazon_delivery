Amazon Delivery Dashboard 
Step 1 — Dataset and Decision-Maker
Dataset: Amazon Delivery Dataset
Source: https://www.kaggle.com/datasets/sujalsuthar/amazon-delivery-dataset
File: amazon_delivery.csv
Size: 8.6 MB
Period: 2022-02-11 to 2022-04-06
One row: A single delivery order, including order time, pickup time, delivery duration, agent information, weather, traffic, area, and product category.

Decision-Maker: Logistics Operations Manager

This manager needs to check every morning whether deliveries are running normally, where they are slow, why they are slow, and whether to adjust dispatch. This is a recurring question that needs a fixed view for quick judgment, which makes it suitable for a dashboard.

Step 2 — Justification
The Logistics Operations Manager looks at this dashboard once every morning, and again when an anomaly appears.

The dashboard supports this decision: if the manager sees that the average delivery time in a certain area or under certain weather/traffic conditions has clearly increased, or that the number of delayed orders has increased for several consecutive days, they will contact the regional dispatch team to adjust rider allocation or issue an early warning.

Today they rely on manual Excel summaries, which lag by 1–2 days. By the time they notice, delayed orders have already piled up and customer complaints have increased.

A dashboard earns its place because the same questions repeat every day, and the manager needs a fixed view to quickly locate the abnormal area and the reason. A weekly report is too slow, and a single alert only covers one threshold without explaining why deliveries are slow.

Step 3 — What Matters
EDA findings
Delivery_Time ranges from 10 to 270 minutes, with a median of 125 and a mean of 124.9. The unit is assumed to be minutes.

Agent_Rating has abnormal values: 1.0 (38 orders) and 6.0 (53 orders). The valid range should be 1–5, so 6.0 is filtered out.

Store_Latitude and Store_Longitude have 3505 rows with value 0.0, which are likely missing or invalid.

Traffic has 91 missing values; Weather has 91 missing values.

Area has 4 categories: Metropolitian (32698), Urban (9751), Other (1138), Semi-Urban (152). The distribution is highly imbalanced.

Order_Time has no missing values, but Order_Time and Pickup_Time only contain time-of-day without date, so some orders appear to have negative pickup gaps when crossing midnight.

What we show
Three headline metrics: average delivery time (mean of Delivery_Time, in minutes), delayed orders (orders with Delivery_Time > 180 minutes), and average agent rating (mean of Agent_Rating). They are shown side by side using st.metric and st.columns.

Two supporting charts: average delivery time by area (explains where deliveries are slow) and average delivery time by weather (explains why deliveries are slow).

Three filters: area, weather, and traffic. These are the dimensions the decision-maker actually uses when investigating an anomaly.

What we chose not to show
We chose not to show a map of every order's latitude and longitude. Although the geographic data exists, the decision-maker cares about which area is slow, not where each order is. A map would add complexity without changing any decision.

We also chose not to show a detailed list of every rider. This is too granular; the decision-maker only needs the overall rating and delivery time, not a per-rider breakdown.

What could mislead the viewer
Delivery_Time unit is not specified in the dataset. We assume it is minutes and state this assumption in the dashboard caption.

Agent_Rating has invalid values (6.0). We filter out ratings above 5 and note this in the caption.

Area is highly imbalanced. Metropolitian accounts for about 75% of orders, while Semi-Urban has only 152 orders. The average delivery time for Semi-Urban is therefore less reliable, and we state this in the dashboard caption.

Order_Time and Pickup_Time lack dates. About 25% of orders show negative pickup gaps due to crossing midnight. This does not affect Delivery_Time, but it means the time fields must be used with caution.

The data covers only Feb 2022 – Apr 2022. A short time window cannot represent a full year.

Page order
The top shows the three headline metrics, answering whether anything is wrong right now.

The middle shows the two supporting charts, explaining why and where deliveries are slow.

The bottom shows an optional detail table, which is omitted if no one uses it.

Step 4 — Refresh Frequency
The data should be refreshed nightly from the logistics system. Delivery data is generated daily, but the decision is made once a day, so real-time refresh adds no extra value and increases cost.

The Operations Manager reviews it once every morning, matching the refresh frequency.

The dashboard should track average delivery time and the number of delayed orders. Action should be triggered when the average delivery time in a certain area stays above 180 minutes for 3 consecutive days, or when the number of delayed orders increases for 3 consecutive days.

Stale data costs time and money: a one-day delay may allow another batch of delayed orders to pile up, increase customer complaints, and put rider dispatch in a passive position.

Dashboard line: Data: Feb 2022 – Apr 2022, Kaggle snapshot. Production refresh: nightly.