import sqlite3
import os
from typing import List, Dict, Optional, Any
from models import User, UserDetail, FilterParams

class Database:
    def __init__(self, db_path: str = "data/leads.db"):
        self.db_path = db_path
        self.ensure_connection()
    
    def ensure_connection(self):
        """Ensure database file exists and is accessible"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        # Test connection
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1")
        except sqlite3.Error as e:
            raise ConnectionError(f"Cannot connect to database: {str(e)}")
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                conn.execute("SELECT 1")
                return True
        except:
            return False
    
    def get_users(self, filters: FilterParams) -> List[User]:
        """Get all unique users with filtering and sorting"""
        with self.get_connection() as conn:
            # Build the query to merge users from both tables
            query = """
            WITH merged_users AS (
                SELECT 
                    uid,
                    user_name,
                    title,
                    linkedin_profile_url,
                    linkedin_image_url,
                    location,
                    req_school,
                    req_country,
                    'schools' as source_table
                FROM leads_schools
                WHERE uid IS NOT NULL AND uid != ''
                
                UNION ALL
                
                SELECT 
                    uid,
                    user_name,
                    title,
                    linkedin_profile_url,
                    linkedin_image_url,
                    location,
                    req_school,
                    req_country,
                    'salesnav' as source_table
                FROM leads_salesnav
                WHERE uid IS NOT NULL AND uid != ''
            ),
            user_sources AS (
                SELECT 
                    uid,
                    GROUP_CONCAT(DISTINCT source_table) as sources,
                    COUNT(DISTINCT source_table) as source_count
                FROM merged_users
                GROUP BY uid
            ),
            unique_users AS (
                SELECT DISTINCT
                    m.uid,
                    COALESCE(NULLIF(m.user_name, ''), 'Unknown User') as user_name,
                    COALESCE(NULLIF(m.title, ''), 'No Title') as title,
                    m.linkedin_profile_url,
                    m.linkedin_image_url,
                    COALESCE(NULLIF(m.location, ''), 'Unknown Location') as location,
                    COALESCE(NULLIF(m.req_school, ''), 'No School') as req_school,
                    COALESCE(NULLIF(m.req_country, ''), 'Unknown Country') as req_country,
                    us.sources,
                    us.source_count
                FROM merged_users m
                JOIN user_sources us ON m.uid = us.uid
            )
            SELECT * FROM unique_users
            WHERE 1=1
            """
            
            params = []
            
            # Add filters
            if filters.search:
                query += " AND (user_name LIKE ? OR title LIKE ? OR location LIKE ?)"
                search_param = f"%{filters.search}%"
                params.extend([search_param, search_param, search_param])
            
            if filters.location_filter:
                query += " AND location LIKE ?"
                params.append(f"%{filters.location_filter}%")
            
            if filters.school_filter:
                query += " AND req_school LIKE ?"
                params.append(f"%{filters.school_filter}%")
            
            if filters.country_filter:
                query += " AND req_country LIKE ?"
                params.append(f"%{filters.country_filter}%")
            
            if filters.source_filter:
                if filters.source_filter == "schools_only":
                    query += " AND sources = 'schools'"
                elif filters.source_filter == "salesnav_only":
                    query += " AND sources = 'salesnav'"
                elif filters.source_filter == "both":
                    query += " AND source_count > 1"
            
            # Add ordering
            valid_columns = ["user_name", "title", "location", "req_school", "req_country"]
            if filters.order_by in valid_columns:
                direction = "DESC" if filters.order_direction.upper() == "DESC" else "ASC"
                query += f" ORDER BY {filters.order_by} {direction}"
            else:
                query += " ORDER BY user_name ASC"
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                # Determine source category and color
                sources = row['sources']
                if 'schools' in sources and 'salesnav' in sources:
                    source_category = "both"
                    color_class = "table-success"
                elif 'schools' in sources:
                    source_category = "schools_only"
                    color_class = "table-info"
                else:
                    source_category = "salesnav_only"
                    color_class = "table-warning"
                
                users.append(User(
                    uid=row['uid'],
                    user_name=row['user_name'],
                    title=row['title'],
                    linkedin_profile_url=row['linkedin_profile_url'],
                    linkedin_image_url=row['linkedin_image_url'],
                    location=row['location'],
                    req_school=row['req_school'],
                    req_country=row['req_country'],
                    source_category=source_category,
                    color_class=color_class
                ))
            
            return users
    
    def get_user_detail(self, uid: str) -> Optional[UserDetail]:
        """Get detailed information for a specific user"""
        with self.get_connection() as conn:
            # Get data from both tables
            schools_query = """
            SELECT * FROM leads_schools WHERE uid = ?
            """
            salesnav_query = """
            SELECT * FROM leads_salesnav WHERE uid = ?
            """
            
            schools_cursor = conn.execute(schools_query, (uid,))
            schools_data = schools_cursor.fetchone()
            
            salesnav_cursor = conn.execute(salesnav_query, (uid,))
            salesnav_data = salesnav_cursor.fetchone()
            
            if not schools_data and not salesnav_data:
                return None
            
            # Merge data preferring non-null values
            def get_value(schools_val, salesnav_val):
                if schools_val and salesnav_val:
                    return schools_val if len(str(schools_val).strip()) > len(str(salesnav_val).strip()) else salesnav_val
                return schools_val or salesnav_val or ""
            
            schools_dict = dict(schools_data) if schools_data else {}
            salesnav_dict = dict(salesnav_data) if salesnav_data else {}
            
            return UserDetail(
                uid=uid,
                user_name=get_value(schools_dict.get('user_name'), salesnav_dict.get('user_name')),
                title=get_value(schools_dict.get('title'), salesnav_dict.get('title')),
                linkedin_profile_url=get_value(schools_dict.get('linkedin_profile_url'), salesnav_dict.get('linkedin_profile_url')),
                linkedin_image_url=get_value(schools_dict.get('linkedin_image_url'), salesnav_dict.get('linkedin_image_url')),
                location=get_value(schools_dict.get('location'), salesnav_dict.get('location')),
                req_school=get_value(schools_dict.get('req_school'), salesnav_dict.get('req_school')),
                req_country=get_value(schools_dict.get('req_country'), salesnav_dict.get('req_country')),
                about=salesnav_dict.get('about', ''),
                headline=salesnav_dict.get('headline', ''),
                skills=salesnav_dict.get('skills', ''),
                experience=salesnav_dict.get('experience', ''),
                in_schools_table=schools_data is not None,
                in_salesnav_table=salesnav_data is not None,
                schools_timestamp=schools_dict.get('timestamp', ''),
                salesnav_timestamp=salesnav_dict.get('timestamp', '')
            )
    
    def get_filter_options(self) -> Dict[str, List[str]]:
        """Get available filter options"""
        with self.get_connection() as conn:
            # Get unique locations
            locations_query = """
            SELECT DISTINCT location FROM (
                SELECT location FROM leads_schools WHERE location IS NOT NULL AND location != ''
                UNION
                SELECT location FROM leads_salesnav WHERE location IS NOT NULL AND location != ''
            ) ORDER BY location
            """
            
            # Get unique schools
            schools_query = """
            SELECT DISTINCT req_school FROM (
                SELECT req_school FROM leads_schools WHERE req_school IS NOT NULL AND req_school != ''
                UNION
                SELECT req_school FROM leads_salesnav WHERE req_school IS NOT NULL AND req_school != ''
            ) ORDER BY req_school
            """
            
            # Get unique countries
            countries_query = """
            SELECT DISTINCT req_country FROM (
                SELECT req_country FROM leads_schools WHERE req_country IS NOT NULL AND req_country != ''
                UNION
                SELECT req_country FROM leads_salesnav WHERE req_country IS NOT NULL AND req_country != ''
            ) ORDER BY req_country
            """
            
            locations = [row[0] for row in conn.execute(locations_query).fetchall()]
            schools = [row[0] for row in conn.execute(schools_query).fetchall()]
            countries = [row[0] for row in conn.execute(countries_query).fetchall()]
            
            return {
                "locations": locations,
                "schools": schools,
                "countries": countries,
                "sources": ["schools_only", "salesnav_only", "both"]
            }
