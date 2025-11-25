import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# 1. Define the Pydantic Schema for the Synthetic Data
# This forces the LLM to generate data in a predictable format for a PRS.
class UserEvent(BaseModel):
    """Schema for a single synthetic user interaction event."""
    user_id: int = Field(description="A unique, non-sensitive integer ID for the user (1 to 10).")
    item_id: str = Field(description="A unique string ID for the item (e.g., 'MOVIE_101', 'BOOK_205').")
    rating: float = Field(description="The user's rating for the item, from 1.0 to 5.0.")
    timestamp: str = Field(description="A fake timestamp string in YYYY-MM-DD HH:MM:SS format.")

# 2. Define the list of events the LLM must return
class UserEventList(BaseModel):
    """The root model containing a list of synthetic user events."""
    events: List[UserEvent]

def generate_synthetic_data(client: genai.Client, num_records: int, profile_description: str) -> List[dict]:
    """
    Generates structured synthetic user data using the Gemini API.

    Args:
        client: The initialized Gemini API client.
        num_records: The number of interaction records to generate.
        profile_description: A description defining the behavior of the users.
    
    Returns:
        A list of dictionaries containing the synthetic data.
    """

    # 3. Construct the System Prompt
    system_prompt = (
        "You are an expert user behavior modeler. Your task is to generate a list of "
        f"{num_records} synthetic user interaction records that perfectly match the "
        "provided JSON schema. The data must accurately reflect the following behavior profile: "
        f"'{profile_description}'. Generate the response as a single, valid JSON object."
    )

    # 4. Configure the API call for structured output (Tool Use)
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=UserEventList,
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Use a fast model
            contents=system_prompt,
            config=config,
        )

        # 5. Parse the JSON response
        if response.text:
            # The API response text is guaranteed to be JSON matching the schema
            data_dict = json.loads(response.text)
            
            # Use the Pydantic model to validate and return the list of events
            validated_data = UserEventList(**data_dict)
            
            # Convert back to a list of standard dictionaries for processing
            return [event.model_dump() for event in validated_data.events]
        else:
            print("Error: API returned an empty response.")
            return []

    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return []