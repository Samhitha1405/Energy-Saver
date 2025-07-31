import joblib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load dataset
df=pd.read_csv("energy_data_india.csv")
st.title("Energy Dashboard")
# Sidebar Filters
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique().tolist()))

if region != "All":
    df = df[df["Region"] == region]
st.subheader(" Household Energy Consumption Overview")
st.write(df.head())

#Metrics
avg_energy = df["Monthly_Energy_Consumption_kWh"].mean()
total_energy = df["Monthly_Energy_Consumption_kWh"].sum()
st.metric("Average Monthly Consumption (kWh)", f"{avg_energy:.2f}")
st.metric("Total Energy Consumption (kWh)", f"{total_energy:.0f}")

# Visualizations
# Energy vs Income
st.subheader(" Income vs Energy Consumption")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh", hue="Region", ax=ax1)
st.pyplot(fig1)

# Appliance Contribution
st.subheader(" Appliance-wise Count vs Energy Consumption")
appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
selected_appliance = st.selectbox("Select Appliance", appliances)
fig2, ax2 = plt.subplots()
sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], ax=ax2)
ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')}")
ax2.set_ylabel("Energy Consumption (kWh)")
st.pyplot(fig2)

#Recommendations
st.subheader(" Smart Recommendations")
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        st.warning(f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs.")
    elif row["EV_Charging"] == 1:
        st.info(f"Household ID {row['Household_ID']} - Consider installing a separate EV meter for optimal billing.")

#Download Recommendations
recommendations = []
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        recommendations.append(f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs.")
    elif row["EV_Charging"] == 1:
        recommendations.append(f"Household ID {row['Household_ID']} - Consider installing a separate EV meter for optimal billing.")

if recommendations:
    st.download_button("Download Recommendations", "\n".join(recommendations), "recommendations.txt")

# Conclusion
# Graphical Analysis Section
st.subheader("Graphical Analysis")
# Distribution of Energy Consumption
st.write("Distribution of Monthly Energy Consumption")

fig_dist, ax_dist = plt.subplots()
sns.histplot(df["Monthly_Energy_Consumption_kWh"], bins=20, kde=True, ax=ax_dist, color='brown')
ax_dist.set_xlabel("Monthly Energy Consumption (kWh)")
ax_dist.set_ylabel("Count")
st.pyplot(fig_dist)

# Boxplot: Energy Consumption by Region
if "Region" in df.columns:
    st.write("Boxplot: Energy Consumption by Region")
    fig_box, ax_box = plt.subplots()
    sns.boxplot(data=df, x="Region", y="Monthly_Energy_Consumption_kWh", ax=ax_box, palette="Set2")
    ax_box.set_xlabel("Region")
    ax_box.set_ylabel("Monthly Energy Consumption (kWh)")
    st.pyplot(fig_box)

# Pie Chart: Households with ACs
if "Appliance_AC" in df.columns:
    st.write("Pie Chart: Households with ACs")
    ac_counts = df["Appliance_AC"].value_counts().sort_index()
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(ac_counts, labels=ac_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax_pie.set_title("Distribution of Number of ACs per Household")
    st.pyplot(fig_pie)
# Load model (outside the main app loop to avoid reloading every run)
model = joblib.load("energy_model.pkl")
st.subheader("Predict Monthly Energy Consumption")
with st.form("prediction_form"):
    income = st.number_input("Monthly Income (INR)", min_value=0)
    ac = st.selectbox("Number of ACs", [0,1,2,3,4])
    fan = st.selectbox("Number of Fans", [0,1,2,3,4])
    light = st.selectbox("Number of Lights", [0,1,2,3,4])
    fridge = st.selectbox("Number of Fridges", [0,1,2])
    washing_machine = st.selectbox("Number of Washing Machines", [0,1,2])
    ev_charging = st.selectbox("EV Charging (0=No,1=Yes)", [0,1])
    submitted = st.form_submit_button("Predict")

    if submitted:
        input_features = pd.DataFrame([[income, ac, fan, light, fridge, washing_machine, ev_charging]],
                                      columns=["Monthly_Income_INR", "Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"])
        prediction = model.predict(input_features)[0]
        st.success(f"Predicted Monthly Energy Consumption: {prediction:.2f} kWh")

def local_css(ap):
    with open(ap)as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call this early in your app
local_css("ap.css")
