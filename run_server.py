import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run("dante_backend.main:app", host="0.0.0.0", port=8000, reload=True)
