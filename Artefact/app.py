import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from flask import Flask, render_template, Response

# Define `app` BEFORE using `@app.route()`
app = Flask(__name__)

# Check if the dataset exists before reading
try:
    df = pd.read_csv('2018-Happiness-Index-Cleaned.csv')
except FileNotFoundError:
    print("CSV file not found! Make sure '2018-Happiness-Index-Cleaned.csv' exists.")
    df = None  # Prevent crashes if the file is missing

non_numeric_columns = ['Country or region']

@app.route('/')
def home():
    print("Home route function started!")

    # If data file is missing, return an error page
    if df is None:
        print("Dataframe is None!")
        return "Error: Data file is missing!", 500

    print("Processing statistics")
    stats_archive = {}

    # Process numeric columns
    for col in df.columns:
        if col not in non_numeric_columns:
            stats_data = pd.to_numeric(df[col], errors='coerce')

            if stats_data.notna().any():
                stats_archive[col] = {
                    'Mean': stats_data.mean(),
                    'Median': stats_data.median(),
                    'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
                    'Range': stats_data.max() - stats_data.min()
                }

    print("Finished processing. Rendering template...")
    return render_template('index.html', stats=stats_archive)

# New route to generate and serve the plot
@app.route('/plot.png')
def plot():
    # Create a simple plot
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4])
    plt.ylabel('Some Numbers')
    plt.title('Sample Plot')

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

# Run Flask only when the script is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=5000)
