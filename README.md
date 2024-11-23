# CarDheko - Used Car Price Prediction

CarDheko - Used Car Price Prediction is a machine learning project developed to enhance the customer experience at Car Dheko by predicting the prices of used cars based on various features. This tool provides an accurate and user-friendly Streamlit application where customers and sales representatives can easily input car features to get real-time price predictions.

## Getting Started

Follow these steps to set up and run CarDheko-Price-Prediction locally.

### Prerequisites

1. **Clone the Repository**  
   Download the repository to your local machine:
   ```bash
   git clone https://github.com/vikashgraja/CarDheko-Price-Prediction.git
   cd CarDheko-Price-Prediction
   ``` 

2. **Install Required Packages**  
   Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ``` 
###  Download the Dataset
The dataset contains multiple Excel files, each representing a different city, and includes detailed information on used cars.

###  Run the data extraction and cleaning code
- Run the extract_data.py to extract the data from the unstructured dataset. 
- Run Data Cleaning.ipynb file to clean the data.

###  Train the model
- Run all the cells in EDA & Model.ipynb file.

###  Running the App
 **Run the Streamlit app:**  
   ```bash
   streamlit run CarDhekoApp.py
   ``` 
