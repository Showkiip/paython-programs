from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
# run_with_ngrok(app)  # Start ngrok when the app is run
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the data
df = pd.read_csv("E:\\MLN\\stackoverflow_full.csv")
df.drop(columns='Unnamed: 0', inplace=True)


# Define a function to segment countries into continents
def segment_country(country):
    if country in ['United States of America', 'Canada', 'Mexico']:
        return 'NorthAmerica'
    elif country in ['United Kingdom of Great Britain and Northern Ireland', 'France', 'Germany', 'Spain', 'Italy',
                     'Portugal', 'Belgium', 'Netherlands', 'Austria', 'Switzerland', 'Denmark', 'Ireland', 'Norway',
                     'Sweden', 'Finland', 'Greece', 'Czech Republic', 'Slovakia', 'Hungary', 'Poland']:
        return 'Europe'
    elif country in ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Venezuela, Bolivarian Republic of...',
                     'Bolivia']:
        return 'South America'
    elif country in ['China', 'Japan', 'South Korea', 'Viet Nam', 'India', 'Sri Lanka', 'Pakistan', 'Bangladesh',
                     'Indonesia', 'Malaysia', 'Philippines', 'Taiwan', 'Thailand', 'Cambodia', 'Myanmar', 'Laos',
                     'Singapore', 'Hong Kong (S.A.R.)']:
        return 'Asia'
    elif country in ['Australia', 'New Zealand', 'Fiji', 'Papua New Guinea', 'Solomon Islands', 'Vanuatu', 'Samoa',
                     'Tonga']:
        return 'Australia'
    else:
        return 'Others'


df['Continent'] = df['Country'].apply(segment_country)

# Create a copy of the original dataframe and label encode categorical columns
df_copy = df.copy()
label_encoder = LabelEncoder()
categorical_columns = ['Age', 'Accessibility', 'EdLevel', 'Gender', 'MentalHealth', 'MainBranch', 'Continent']
for col in categorical_columns:
    df_copy[col] = label_encoder.fit_transform(df[col])


@app.route('/api/get_encoded_data', methods=['GET'])
def get_data():
    # Extract query parameters
    filters = {k: v for k, v in request.args.items() if v}

    # Filter dataframe based on provided parameters
    filtered_df = df.copy()
    for col, value in filters.items():
        if col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(value, case=False, na=False)]

    return jsonify({
        "columns": filtered_df.columns.tolist(),
        "missing_values": filtered_df.isna().sum().to_dict(),
        "unique_continents": filtered_df.Continent.unique().tolist(),
        "head": filtered_df.head().to_dict(orient='records')
    })


@app.route('/api/get_encoded_data', methods=['GET'])
def get_encoded_data():
    # Extract query parameters
    filters = {k: v for k, v in request.args.items() if v}

    # Filter dataframe based on provided parameters
    filtered_df_copy = df_copy.copy()
    for col, value in filters.items():
        if col in filtered_df_copy.columns:
            filtered_df_copy = filtered_df_copy[
                filtered_df_copy[col].astype(str).str.contains(value, case=False, na=False)]

    return jsonify({
        "encoded_columns": categorical_columns,
        "head_encoded": filtered_df_copy.head().to_dict(orient='records')
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
