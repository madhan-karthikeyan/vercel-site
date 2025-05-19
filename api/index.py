from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import List, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Path to data file
data_path = os.path.join(os.path.dirname(__file__), 'data.json')

@app.get("/")
async def get_marks(name: Optional[List[str]] = Query(None)):
    """
    Get marks for the specified names.
    
    Parameters:
    - name: List of names to get marks for
    
    Returns:
    - Dictionary with a 'marks' list containing marks for each name in the same order
    """
    try:
        # Load the data
        with open(data_path, 'r') as file:
            data = json.load(file)
        
        # Create name-to-marks mapping
        name_to_marks = {item["name"]: item["marks"] for item in data}
        
        # Get marks for each name
        marks = []
        if name:
            for n in name:
                if n in name_to_marks:
                    marks.append(name_to_marks[n])
                else:
                    marks.append(None)
        
        # Return the result
        return {"marks": marks}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
