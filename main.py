from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Optional
import uvicorn
from database import Database
from models import User, UserDetail, FilterParams

app = FastAPI(title="Leads Management System", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database
db = Database()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/users", response_model=List[User])
async def get_users(
    search: Optional[str] = None,
    location_filter: Optional[str] = None,
    school_filter: Optional[str] = None,
    country_filter: Optional[str] = None,
    source_filter: Optional[str] = None,
    order_by: Optional[str] = "user_name",
    order_direction: Optional[str] = "ASC"
):
    """Get all unique users with filtering and sorting"""
    try:
        filters = FilterParams(
            search=search,
            location_filter=location_filter,
            school_filter=school_filter,
            country_filter=country_filter,
            source_filter=source_filter,
            order_by=order_by,
            order_direction=order_direction
        )
        users = db.get_users(filters)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/users/{uid}", response_model=UserDetail)
async def get_user_detail(uid: str):
    """Get detailed information for a specific user"""
    try:
        user_detail = db.get_user_detail(uid)
        if not user_detail:
            raise HTTPException(status_code=404, detail="User not found")
        return user_detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/filters")
async def get_filter_options():
    """Get available filter options"""
    try:
        options = db.get_filter_options()
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": db.test_connection()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
