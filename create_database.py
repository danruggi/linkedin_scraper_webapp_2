import sqlite3
import os

# Create database directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Create the database and tables
conn = sqlite3.connect("data/leads.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS leads_schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT,
    uid TEXT UNIQUE,
    user_name TEXT,
    linkedin_profile_url TEXT,
    linkedin_image_url TEXT,
    title TEXT,
    location TEXT,
    req_school TEXT,
    req_country TEXT,
    timestamp TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS leads_salesnav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT,
    uid TEXT UNIQUE,
    user_name TEXT,
    linkedin_profile_url TEXT,
    linkedin_image_url TEXT,
    title TEXT,
    location TEXT,
    about TEXT,
    headline TEXT,
    skills TEXT,
    experience TEXT,
    req_school TEXT,
    req_country TEXT,
    timestamp TEXT
);
''')

# Insert sample data
sample_schools_data = [
    ('john-doe', 'user_001', 'John Doe', 'https://linkedin.com/in/johndoe', 'https://media.licdn.com/dms/image/sample1.jpg', 'Software Engineer', 'San Francisco, CA', 'Stanford University', 'USA', '2024-01-15 10:30:00'),
    ('jane-smith', 'user_002', 'Jane Smith', 'https://linkedin.com/in/janesmith', 'https://media.licdn.com/dms/image/sample2.jpg', 'Product Manager', 'New York, NY', 'Harvard University', 'USA', '2024-01-16 14:20:00'),
    ('michael-brown', 'user_003', 'Michael Brown', 'https://linkedin.com/in/michaelbrown', None, 'Data Scientist', 'London, UK', 'Oxford University', 'UK', '2024-01-17 09:45:00'),
    ('emily-davis', 'user_006', 'Emily Davis', 'https://linkedin.com/in/emilydavis', 'https://media.licdn.com/dms/image/sample4.jpg', 'Marketing Manager', 'Boston, MA', 'MIT', 'USA', '2024-01-21 08:15:00'),
    ('robert-wilson', 'user_007', 'Robert Wilson', 'https://linkedin.com/in/robertwilson', None, 'Sales Director', 'Toronto, ON', 'University of Toronto', 'Canada', '2024-01-22 12:00:00'),
]

sample_salesnav_data = [
    ('jane-smith', 'user_002', 'Jane Smith', 'https://linkedin.com/in/janesmith', 'https://media.licdn.com/dms/image/sample2.jpg', 'Senior Product Manager', 'New York, NY', 'Experienced product manager with 8+ years in tech startups', 'Building innovative products that users love', 'Product Management, Strategy, Analytics', 'Senior PM at TechCorp (2020-present), PM at StartupXYZ (2018-2020)', 'Harvard University', 'USA', '2024-01-18 11:15:00'),
    ('david-wilson', 'user_004', 'David Wilson', 'https://linkedin.com/in/davidwilson', 'https://media.licdn.com/dms/image/sample3.jpg', 'Marketing Director', 'Chicago, IL', 'Marketing professional specializing in digital campaigns', 'Driving growth through data-driven marketing', 'Digital Marketing, SEO, Analytics', 'Marketing Director at BigCorp (2019-present)', 'Northwestern University', 'USA', '2024-01-19 16:30:00'),
    ('sarah-johnson', 'user_005', 'Sarah Johnson', 'https://linkedin.com/in/sarahjohnson', None, 'UX Designer', 'Austin, TX', 'Creative designer focused on user experience', 'Designing beautiful and functional interfaces', 'UX Design, Prototyping, User Research', 'UX Designer at DesignStudio (2021-present)', 'University of Texas', 'USA', '2024-01-20 13:45:00'),
    ('alex-chen', 'user_008', 'Alex Chen', 'https://linkedin.com/in/alexchen', 'https://media.licdn.com/dms/image/sample5.jpg', 'Data Analyst', 'Seattle, WA', 'Data analyst with expertise in machine learning and statistics', 'Turning data into actionable insights', 'Python, SQL, Machine Learning, Statistics', 'Data Analyst at DataCorp (2022-present)', 'University of Washington', 'USA', '2024-01-23 14:30:00'),
    ('maria-garcia', 'user_009', 'Maria Garcia', 'https://linkedin.com/in/mariagarcia', None, 'HR Manager', 'Mexico City, MX', 'Human resources professional focused on talent acquisition', 'Building great teams and company culture', 'HR Management, Recruitment, Employee Relations', 'HR Manager at GlobalTech (2021-present)', 'Universidad Nacional Autónoma de México', 'Mexico', '2024-01-24 10:45:00'),
]

cursor.executemany('''
INSERT OR IGNORE INTO leads_schools (slug, uid, user_name, linkedin_profile_url, linkedin_image_url, title, location, req_school, req_country, timestamp)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_schools_data)

cursor.executemany('''
INSERT OR IGNORE INTO leads_salesnav (slug, uid, user_name, linkedin_profile_url, linkedin_image_url, title, location, about, headline, skills, experience, req_school, req_country, timestamp)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_salesnav_data)

conn.commit()
conn.close()

print("Database created successfully with sample data!")
print("Tables created: leads_schools, leads_salesnav")
print(f"Sample data inserted: {len(sample_schools_data)} school records, {len(sample_salesnav_data)} salesnav records")