import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import plotly.graph_objects as go

# Load the data
merged_df = pd.read_csv("https://raw.githubusercontent.com/bahau88/G2Elab-Energy-Building-/main/dataset/combined_data_green-er_2020_2023.csv")
#merged_df['Date'] = pd.to_datetime(merged_df['Date'])
#merged_df.set_index('Date', inplace=True)

# Define features and target
features = ['Number of Room', 'Dayindex', 'Occupants', 'Temperature', 'Cloudcover', 'Visibility']
target = 'Consumption'

# Function to train and evaluate the model
def train_and_evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return model, y_pred, r2

# Function to plot feature importances
def plot_feature_importances(features, importances):
    fig = go.Figure([go.Bar(x=features, y=importances, text=importances, textposition='auto', textfont=dict(size=12))])
    fig.update_layout(
        title='Feature Importances',
        xaxis_title='Feature',
        yaxis_title='Importance',
        font=dict(size=12),
        plot_bgcolor='white',
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig)

# Streamlit app
st.title("Feature Importance")
method = st.selectbox("Select Method", ["Random Forest", "Gradient Boosting", "Decision Tree"])
test_size = st.slider("Select Test Size", 0.1, 0.4, step=0.1)

if st.button("Train and Evaluate"):
    X = merged_df[features]
    y = merged_df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    if method == "Random Forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif method == "Gradient Boosting":
        model = GradientBoostingRegressor()
    else:
        model = DecisionTreeRegressor()
    
    trained_model, y_pred, r2 = train_and_evaluate_model(model, X_train, X_test, y_train, y_test)
    
    st.write("R2 score:", r2)
    plot_feature_importances(features, trained_model.feature_importances_)
