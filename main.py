import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from data_generator import generate_synthetic_data

# --- Configuration ---
# 1. Load variables from the .env file into the environment
load_dotenv() 

# 2. Retrieve the key from the environment (loaded from .env)
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_KEY_NOT_FOUND")

# Ensure the output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Define Synthetic Profiles ---
PROFILES = {
    "tech_enthusiast": {
        "description": "Users who highly rate new tech gadgets (items with ID starting 'GADGET_') and rarely rate books.",
        "records": 50
    },
    "fitness_nut": {
        "description": "Users who frequently give 5.0 ratings to health/fitness apps and equipment (items starting 'FIT_') but often give low ratings (1.0-2.0) to fast food.",
        "records": 50
    }
}

def main():
    if API_KEY == "YOUR_KEY_NOT_FOUND":
        print("ERROR: GEMINI_API_KEY not found. Please check your .env file or environment variables.")
        return

    try:
        # Initialize the client
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Failed to initialize Gemini client: {e}")
        return

    print("--- Starting Synthetic Data Generation ---")
    all_data = []

    for name, profile in PROFILES.items():
        print(f"\nGenerating {profile['records']} records for: {name}...")
        
        synthetic_records = generate_synthetic_data(
            client=client,
            num_records=profile['records'],
            profile_description=profile['description']
        )
        
        if synthetic_records:
            print(f"Successfully generated {len(synthetic_records)} records.")
            
            # Add a column to identify the generated profile
            df = pd.DataFrame(synthetic_records)
            df['profile_type'] = name
            all_data.append(df)
        else:
            print(f"Skipping profile {name} due to generation error.")

    if all_data:
        # Combine all data into a single DataFrame
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Save the final synthetic dataset to CSV
        output_path = os.path.join(OUTPUT_DIR, "synthetic_prs_data.csv")
        final_df.to_csv(output_path, index=False)
        
        print("\n--- Generation Complete ---")
        print(f"Total records generated: {len(final_df)}")
        print(f"Data saved to: {output_path}")

if __name__ == "__main__":
    main()