from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Connect to Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

app = FastAPI()

# Define what a trade looks like
class Trade(BaseModel):
    entry_date: str  # e.g., "2025-12-22T14:30:00Z"
    pair: str | None = None
    entry_time: str | None = None
    entry_type: str | None = None
    rr: str | None = None
    feedback: str | None = None
    what_did_i_do_wrong: str | None = None
    entry_ss: str | None = None

@app.get("/")
def root():
    return {"message": "JournalForge Backend Connected! 🚀"}

@app.post("/trades")
def create_trade(trade: Trade):
    try:
        data = trade.dict(exclude_unset=True)  # Only send filled fields
        response = supabase.table("trades").insert(data).execute()
        
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=400, detail=str(response.error))
        
        if response.data:
            return {"message": "Trade saved successfully!", "id": response.data[0]["id"]}
        else:
            raise HTTPException(status_code=400, detail="No data returned from Supabase")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")