# app/dashboard.py
import streamlit as st
import requests

st.title("ML Model Dashboard")

st.header("Train a Model")
model_type = st.selectbox("Select Model Type", ["decision_tree", "random_forest"])
params = st.text_area("Enter Hyperparameters (JSON format)")
train_button = st.button("Train Model")

if train_button:
    params_dict = eval(params)
    response = requests.post("http://localhost:8000/train", json={"type_of_model": model_type, "parameters": params_dict})
    st.write(response.json())
