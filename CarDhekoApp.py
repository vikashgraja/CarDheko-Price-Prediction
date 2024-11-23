import streamlit as st
import pandas as pd
import joblib

test_input = pd.DataFrame({
    'Fuel type': ['Petrol'],
    'body type': ['SUV'],
    'transmission': ['Manual'],
    'ownerNo': [1],
    'Brand': ['Hyundai'],
    'model': ['Hyundai Verna'],
    'modelYear': [2024],
    'Year of Manufacture': [2024],
    'Insurance Validity': ['Third Party insurance'],
    'km': [0],
    'Mileage': [16.8],
    'Engine': [8000],
    'Seats': [5],
    'Color': ['White'],
    'Gear Box': ['7-Speed'],
    'city': ['chennai']  # Adjust case for consistency
})

# Load model and encoder
model = joblib.load('car_price_predictor.pkl')
encoder_label = joblib.load('encoder.pkl')  # Dictionary of encoded labels

# Columns that require dropdowns
dropdown_columns = ['Fuel type', 'body type', 'transmission', 'Brand', 'model',
                    'Insurance Validity', 'Color', 'Gear Box', 'city']

# Function to reverse encode for dropdown options
def get_dropdown_options(encoder_label, columns):
    dropdown_options = {}
    for col in columns:
        if col in encoder_label:
            # Reverse the encoding dictionary
            dropdown_options[col] = {v: k for k, v in encoder_label[col].items()}
    return dropdown_options

def label_encode_input(input_data, encoder_label):
    encoded_data = input_data.copy()
    for col, mapping in encoder_label.items():
        if col in encoded_data.columns:
            encoded_data[col] = encoded_data[col].map(mapping)
    return encoded_data

# Get dropdown options
dropdown_options = get_dropdown_options(encoder_label, dropdown_columns)

# Streamlit App UI
st.title("Car Price Prediction")

# Collect user input
st.header("Enter Car Details:")
user_input = {}

for col in dropdown_columns:
    options = list(dropdown_options[col].values())
    user_input[col] = st.selectbox(f"Select {col}", options)

# Numerical input fields
numerical_columns = ['ownerNo', 'modelYear', 'Year of Manufacture', 'km', 'Mileage', 'Engine', 'Seats']
for col in numerical_columns:
    user_input[col] = st.number_input(f"Enter {col}", min_value=0, step=1)

# Button to predict price
if st.button("Predict Price"):
    try:
        # Prepare input DataFrame
        input_data = pd.DataFrame([user_input])
        input_data=input_data[test_input.columns]
        # Encode dropdown inputs
        input_data = label_encode_input(input_data, encoder_label)

        # Check for missing values due to unmapped inputs
        if input_data.isnull().any().any():
            st.error("Invalid input detected. Please ensure all inputs are correct.")
        else:
            # Predict price
            predicted_price = model.predict(input_data)
            st.success(f"Predicted Price: ₹{round(predicted_price[0], 2)}")
    except Exception as e:
        st.error(f"An error occurred: {e}")