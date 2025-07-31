# Energy-Saver
Interactive dashboard for analyzing and predicting household energy use

# ⚡ Energy Dashboard — Streamlit App

An interactive dashboard to analyze, visualize, and predict household energy consumption in India. Built with **Streamlit**, it features data filtering, smart recommendations, and an integrated ML model for consumption prediction.


## 🚀 Features
- Region-wise data filtering
- Visual insights: income vs energy usage, appliance impact
- Smart energy-saving recommendations
- ML-based consumption prediction
- Downloadable tips for households
- Custom-styled UI with CSS

**Project Structure**

energy-dashboard/
├── app.py # Main Streamlit app
├── energy_data_india.csv # Dataset
├── energy_model.pkl # Trained ML model (Random Forest)
├── styles.css # Custom CSS styling
├── requirements.txt # Python dependencies

**INSTALL DEPENDENCIES**
pip install -r requirements.txt
Run the app locally:

streamlit run app.py

🧠 Machine Learning
The app uses a Random Forest model (energy_model.pkl) trained to predict monthly energy consumption based on:
Monthly income
Appliance ownership (AC, Fan, Fridge, etc.)
EV charging status

