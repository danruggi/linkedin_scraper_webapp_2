# Leads Management System

## Overview

This is a web-based Leads Management System built with FastAPI backend and vanilla JavaScript frontend. The system manages and displays lead data from multiple sources (schools and sales navigator), allowing users to filter, search, and view detailed information about leads stored in a SQLite database.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI (Python web framework)
- **Database**: SQLite with direct SQL queries
- **Template Engine**: Jinja2 for HTML rendering
- **Data Models**: Pydantic models for request/response validation
- **API Design**: RESTful endpoints with proper error handling

### Frontend Architecture
- **Technology**: Vanilla JavaScript with jQuery
- **UI Framework**: Bootstrap 5 for responsive design
- **Data Tables**: DataTables.js for enhanced table functionality
- **Icons**: Font Awesome for UI icons
- **Architecture Pattern**: Class-based JavaScript organization

### Database Design
- **Type**: SQLite file-based database
- **Tables**: Two main tables (schools and salesnav) that are merged for unified user view
- **Key Fields**: uid (unique identifier), user details, LinkedIn profiles, location data
- **Data Merging**: Complex SQL queries to combine data from both sources

## Key Components

### Backend Components
1. **Database Layer** (`database.py`)
   - Handles SQLite connections and queries
   - Implements filtering, sorting, and data merging logic
   - Provides connection testing and error handling

2. **API Layer** (`main.py`)
   - FastAPI application with REST endpoints
   - Serves both API endpoints and HTML templates
   - Handles user listing and detail retrieval

3. **Data Models** (`models.py`)
   - Pydantic models for data validation
   - User, UserDetail, and FilterParams classes
   - Ensures type safety and API documentation

### Frontend Components
1. **Main Application** (`static/js/app.js`)
   - LeadsManager class for application state management
   - Handles filtering, searching, and UI interactions
   - Manages DataTables integration

2. **User Interface** (`templates/index.html`)
   - Bootstrap-based responsive design
   - Filter controls and search functionality
   - DataTables integration for enhanced table features

3. **Styling** (`static/css/styles.css`)
   - Custom CSS variables for consistent theming
   - Enhanced card and table styling
   - Responsive design improvements

## Data Flow

1. **User Request**: User accesses the web interface or API endpoints
2. **Filter Processing**: Frontend collects filter parameters and sends to backend
3. **Database Query**: Backend constructs SQL queries based on filters
4. **Data Merging**: System combines data from schools and salesnav tables
5. **Response**: Formatted data returned to frontend
6. **Display**: Frontend renders data in DataTables with sorting/filtering

## External Dependencies

### Backend Dependencies
- FastAPI for web framework
- Uvicorn for ASGI server
- Pydantic for data validation
- Jinja2 for templating
- SQLite3 (built-in Python)

### Frontend Dependencies
- Bootstrap 5 (CSS framework)
- jQuery (JavaScript library)
- DataTables.js (table enhancement)
- Font Awesome (icons)

## Deployment Strategy

### Current Setup
- SQLite database stored in `data/leads.db`
- Static files served through FastAPI
- Single-server deployment model

### Production Considerations
- Database file must exist before application start
- Static files served from `/static` directory
- Templates served from `/templates` directory
- Environment-specific database paths supported

### Key Architectural Decisions

1. **SQLite Choice**: Chosen for simplicity and file-based storage, suitable for moderate data volumes
2. **Data Merging Strategy**: Complex SQL queries to combine two data sources into unified view
3. **Frontend Framework**: Vanilla JavaScript chosen over heavy frameworks for simplicity
4. **Filtering Architecture**: Server-side filtering with client-side enhancement through DataTables
5. **Color Coding System**: Bootstrap color classes used to indicate data source origin