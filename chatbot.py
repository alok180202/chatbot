import requests
import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import numpy as np  # Import numpy for generating random data
import matplotlib.pyplot as plt

# Your Google Gemini API key
api_key = 'AIzaSyDcavMnxK8otspxPiKB0iUYf_4ASohiWiM'

# The URL for the Google Gemini API endpoint
api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

def generate_response(disease_name):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"What are the symptoms of {disease_name}?"
                    }
                ]
            }
        ]
    }

    response = requests.post(f'{api_url}?key={api_key}', headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        try:
            return response_json['candidates'][0]['content']['parts'][0]['text'].strip()
        except KeyError as e:
            return f"Unexpected response structure: {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"

def fetch_disease_data(disease_name):
    # Dummy data to simulate the number of cases in the last month
    data = {
        'Date': pd.date_range(start='2024-07-01', end='2024-07-31'),
        'Cases': np.random.randint(50, 200, size=31)  # Random data for demonstration
    }
    df = pd.DataFrame(data)
    return df

def display_symptoms():
    disease_name = disease_entry.get()
    if disease_name:
        symptoms = generate_response(disease_name)
        df = fetch_disease_data(disease_name)
        
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Symptoms of {disease_name}:\n\n{symptoms}\n\n")
        text_area.insert(tk.END, f"Disease Data:\n\n{df.to_string(index=False)}")
        text_area.config(state=tk.DISABLED)
        
        plot_graph(df, disease_name)

def plot_graph(df, disease_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Cases'], marker='o', linestyle='-', color='b')
    plt.title(f'Number of {disease_name} Cases in India (Last Month)')
    plt.xlabel('Date')
    plt.ylabel('Number of Cases')
    plt.grid(True)
    plt.show()

# Setting up the GUI window
window = tk.Tk()
window.title("Medical Symptom Bot")

# Label
label = tk.Label(window, text="Enter a medical disease:")
label.pack(pady=10)

# Entry box
disease_entry = tk.Entry(window, width=50)
disease_entry.pack(pady=5)

# Button
button = tk.Button(window, text="Get Symptoms and Data", command=display_symptoms)
button.pack(pady=10)

# ScrolledText widget to display the output
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
text_area.pack(padx=10, pady=10)

# Running the GUI loop
window.mainloop()
