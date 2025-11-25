## Privacy Data Synthesizer

### Project Summary

Privacy Data Synthesizer is a proof-of-concept project that tackles the core challenge of **data privacy in personalized machine learning** by generating statistically realistic, yet entirely synthetic, user interaction data.

It leverages the structured output capabilities of the **Gemini Large Language Model (LLM)** to simulate complex user behavior profiles, such as "Tech Enthusiast" or "Fitness Nut," and output the results in a strict, machine-readable format (CSV).

### Purpose

This tool is designed to provide **privacy-safe datasets** for the development, testing, and debugging of **Federated Learning (FL) algorithms**—like **FedProx**—and **Personalized Recommendation Systems (PRS)**. By relying on generated data instead of sensitive production records, PriSyn enables researchers and developers to iterate rapidly while maintaining compliance with privacy standards.

### Key Features

* **Privacy-Preserving:** Generates data based on descriptive profiles, eliminating the use of actual PII (Personally Identifiable Information).
* **Structured Output:** Uses Pydantic schemas and Gemini's function calling to guarantee clean, structured CSV data for direct model ingestion.
* **Behavioral Modeling:** Simple descriptive prompts define complex synthetic user behaviors (e.g., specific rating patterns, item preferences).
* **Secure API Handling:** Uses a `.env` file for secure management of the Gemini API key.

### Technologies

* **LLM:** Google Gemini API (`gemini-2.5-flash`)
* **Framework:** Python
* **Libraries:** `google-genai`, `pydantic`, `pandas`, `python-dotenv`

data_generator.py file defines the data structure using Pydantic and contains the function that interacts with the Gemini API to force structured output.

main.py file sets up the API client, defines the custom profiles, and saves the output.

# Output
<img width="597" height="352" alt="image" src="https://github.com/user-attachments/assets/d030e1dd-2e03-47ba-a929-913bbef0c140" />
<img width="707" height="629" alt="image" src="https://github.com/user-attachments/assets/8584e17f-f6a6-4a12-b1cc-720936f3e2d2" />

