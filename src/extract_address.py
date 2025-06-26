from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import requests
import json
import os
from src.config import ADDRESS_JSON_PATH
from src.geo_location_update import update_from_partial_address

load_dotenv()

class Address(BaseModel):
    zipcode: Optional[str] = Field(description="Zip Code / Postal Code in the sentence")
    house_no: Optional[int] = Field(description="House No / Flat No / Building No / Apartment No in the sentence")
    street: Optional[str] = Field(description="Street / Avenue / Road / Drive in the sentence")
    unit: Optional[str] = Field(description="Apartment / Unit / Suite number in the sentence")
    landmark: Optional[str] = Field(description="Any landmark in the sentence")
    borough: Optional[str] = Field(description="Borough (e.g., Brooklyn, Manhattan) if applicable")
    county: Optional[str] = Field(description="County / administrative area")
    city: Optional[str] = Field(description="City / Town / Municipality")
    state: Optional[str] = Field(description="State or State abbreviation")
    country: Optional[str] = Field(default="United States", description="Country name (default to USA)")

# Initialize the Groq LLM via langchain_groq
llm = ChatGroq(model="gemma2-9b-it", temperature=0)

parser = PydanticOutputParser(pydantic_object=Address)

def extract_address(transcription: str):
    prompt = PromptTemplate(
        template="""
You are an address extraction system optimized for parsing addresses from the United States.

Your task is to extract structured address details from free-form English text using intelligent parsing, spelling correction, and logical inference. Return the result as a valid **JSON object** with the following keys **exactly and only**:

- zipcode  
- house_no  
- street  
- unit  
- landmark    
- borough  
- county  
- city  
- state  
- country

### Rules:

1. Fix spelling mistakes (e.g., "New Yrok" → "New York").
2. Use ZIP code to infer city and state where applicable.
3. If any field is missing or cannot be inferred, return `null`.
4. Output must be valid JSON only — no extra text.
5. Capitalize proper nouns correctly.
6. Convert written numbers to digits (e.g., "twenty one" → 21).
7. Assume U.S. address formatting.
8. Prefer official U.S. geographic terms for city, borough, and county.

### Example Input:
I live at 123 Maple Avenue, ZIP 10001, near Madison Square Garden in New York.

### Expected Output:
```json
{{
  "zipcode": "10001",
  "house_no": 123,
  "street": "Maple Avenue",
  "unit": null,
  "landmark": "Madison Square Garden",
  "borough": null,
  "county": null,
  "city": "New York",
  "state": "New York",
  "country": "United States"
}}

```
Now extract from this text:
{transcription}\n {format_instructions}
""",
input_variables=["transcription"],
partial_variables={'format_instructions': parser.get_format_instructions()}
)
    
    chain = prompt | llm | parser

    # Query the LLM
    result = chain.invoke({'transcription': transcription})
    
    # Debug print raw output
    print("Raw LLM output:", result)

    return (result)




def main(text):
    file_path = ADDRESS_JSON_PATH

    if os.path.exists(file_path):
        os.remove(file_path)

    extracted = extract_address(text)
    print("\nExtracted Address:", extracted)

    # Save to JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        # json.dump(extracted.dict(), f, indent=4, ensure_ascii=False)
        json.dump(extracted.model_dump(), f, indent=4, ensure_ascii=False)

    print(f"\nAddress saved to {file_path}")

    # Update city/state from pincode using API
    update_from_partial_address(file_path)


if __name__=="__main__":
    # text = "My name is XYZ. I live in Mujuffarnagar, at location of house no 132, lane seven, saket, 251001"
    # text = "Muzaffarnagar, India"
    # text = "my pin code is 10002 house number 23 in USA"
    # text = "My zip code is 10011 and I am from USA."
    text = "I live at 742 Evergreen Terrace, Springfield, ZIP 62704, near the Kwik-E-Mart"
    
    main(text)
