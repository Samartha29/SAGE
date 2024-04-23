# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('marks_dataset.csv')

# Split the data into features (X) and target variable (y)
X = data[['QUIZ1', 'QUIZ2', 'ASSIGNMENT', 'MIDSEM']]
y = data['ENDSEM']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize marks to the range [0, 1]
X_train_normalized = X_train / 100.0
X_test_normalized = X_test / 100.0

# Train Linear Regression model
linear_model = LinearRegression()
linear_model.fit(X_train_normalized, y_train)

# Train Random Forest Regression model
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train_normalized, y_train)

# Train Support Vector Regression model
svr_model = SVR()
svr_model.fit(X_train_normalized, y_train)

# Train Gradient Boosting Regression model
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train_normalized, y_train)

# Make predictions
linear_predictions = linear_model.predict(X_test_normalized)
rf_predictions = rf_model.predict(X_test_normalized)
svr_predictions = svr_model.predict(X_test_normalized)
gb_predictions = gb_model.predict(X_test_normalized)

# Streamlit UI
st.title('ENDSEM Score Prediction')

# Input section
st.sidebar.header('Enter Marks for Prediction')
quiz1 = st.sidebar.slider('QUIZ1', min_value=0, max_value=100, value=50)
quiz2 = st.sidebar.slider('QUIZ2', min_value=0, max_value=100, value=50)
assignment = st.sidebar.slider('ASSIGNMENT', min_value=0, max_value=100, value=50)
midsem = st.sidebar.slider('MIDSEM', min_value=0, max_value=100, value=50)

# Normalize input marks to the range [0, 1]
input_marks = [quiz1, quiz2, assignment, midsem]
input_marks_normalized = [mark / 100.0 for mark in input_marks]

# Predictions
linear_prediction = linear_model.predict([input_marks_normalized])
rf_prediction = rf_model.predict([input_marks_normalized])
svr_prediction = svr_model.predict([input_marks_normalized])
gb_prediction = gb_model.predict([input_marks_normalized])

# Display predictions
st.subheader('Predicted ENDSEM Score:')
# Highlight the best model in green
best_model = min([(mean_squared_error(y_test, linear_predictions), 'Linear Regression'), 
                  (mean_squared_error(y_test, rf_predictions), 'Random Forest Regression'), 
                  (mean_squared_error(y_test, linear_predictions), 'Support Vector Regression'), 
                  (mean_squared_error(y_test, linear_predictions), 'Gradient Boosting Regression')])

for model_pred, model_name in [(linear_prediction[0], 'Linear Regression'), 
                               (rf_prediction[0], 'Random Forest Regression'), 
                               (svr_prediction[0], 'Support Vector Regression'), 
                               (gb_prediction[0], 'Gradient Boosting Regression')]:
    if model_name == best_model[1]:
        st.write(f'<span style="color:green">{model_name}: <b>{model_pred:.2f}</b></span>', unsafe_allow_html=True, key=model_name)
    else:
        st.write(f'{model_name}: **{model_pred:.2f}**')

# Evaluation
st.subheader('Model Evaluation (Mean Squared Error):')
st.write(f'Linear Regression: {mean_squared_error(y_test, linear_predictions):.2f}')
st.write(f'Random Forest Regression: {mean_squared_error(y_test, rf_predictions):.2f}')
st.write(f'Support Vector Regression: {mean_squared_error(y_test, svr_predictions):.2f}')
st.write(f'Gradient Boosting Regression: {mean_squared_error(y_test, gb_predictions):.2f}')

# # Plotting
# st.subheader('Actual vs. Predicted (Random Forest Regression)')
# fig, ax = plt.subplots()
# ax.scatter(y_test, rf_predictions)
# ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], linestyle='--', color='red', linewidth=2)  # Identity line
# ax.set_xlabel('Actual ENDSEM Score')
# ax.set_ylabel('Predicted ENDSEM Score')
# st.pyplot(fig)
