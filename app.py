from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import os
import json
from main import main
from src.config import ADDRESS_JSON_PATH, INDEX_HTML_PATH, AUDIO_FOLDER

app = FastAPI()

# Ensure audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Serve your index.html at "/"
@app.get("/", response_class=FileResponse)
async def index():
    if os.path.exists(INDEX_HTML_PATH):
        return FileResponse(INDEX_HTML_PATH)
    else:
        raise HTTPException(status_code=404, detail="Index file not found")

# Submit address form route
@app.post("/submit-address", response_class=PlainTextResponse)
async def submit_address(
    zipcode: str = Form(None),
    house_no: str = Form(None),
    street: str = Form(None),
    unit: str = Form(None),
    landmark: str = Form(None),
    borough: str = Form(None),
    county: str = Form(None),
    city: str = Form(None),
    state: str = Form(None),
    country: str = Form(None),
):
    address = {
        "zipcode": zipcode,
        "house_no": house_no,
        "street": street,
        "unit": unit,
        "landmark": landmark,
        "borough": borough,
        "county": county,
        "city": city,
        "state": state,
        "country": country,
    }
    print("Address Received:", address)
    return "Address saved!"

# Upload audio file route
@app.post("/upload", response_class=PlainTextResponse)
async def upload(audio: UploadFile = File(...)):
    filepath = os.path.join(AUDIO_FOLDER, audio.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await audio.read())
    main()  # You may want to adapt main() to async if needed
    return "Audio received and saved."

# Get address JSON route
@app.get("/get-address")
async def get_address():
    if os.path.exists(ADDRESS_JSON_PATH):
        with open(ADDRESS_JSON_PATH, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    else:
        return JSONResponse(status_code=404, content={"error": "Address file not found"})

app.mount("/static", StaticFiles(directory="static"), name="static")
