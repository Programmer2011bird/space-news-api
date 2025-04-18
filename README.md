# SPACE NEW API
A RESTFUL API made for serving space and physics related articles from space.com

## Data Source & Disclaimer
Articles are sourced from Space.com for **personal, non-commercial use only**.  
This project complies with fair use (not republishing full content for profit).

## Features :

### Data
- Full article content including title, body, author, date etc.
- Summary of the article ( given by space.com )
- Article Categories
- Links to the original article

### Filtering Endpoints
| Endpoint | Description |
|----------|-------------|
| `/` or `/daily` | Daily news | 
| `/search/date/{year}-{month}-{day}` | News from a specific date |
| `/search/dates/start_date={year}-{month}-{day}&end_date={year}-{month}-{day}` | News from a specific date range | 
| `/search/category/{name}` | Category filter | 
| `/search/keyword/{query}` | Title keyword search |
| `/author/{name}` | Articles by author | 

## Tech stack
- **Backend** : FastAPI
- **Database** : PostgreSQL
- **Scraping** : BeautifulSoup + requests

## Other
- **Rate Limiting** : 100 requests every hour
- **Daily scraping** : Scraping news every 1AM and 6PM

### Get started
```sql
-- Database configuration
CREATE DATABASE news;

\c news

CREATE TABLE news (
    name VARCHAR(1040),
    category VARCHAR(255),
    date date,
    link text,
    summary text,
    article_content text,
    author VARCHAR(255)
)

-- Automatic tsvector search

ALTER TABLE news ADD COLUMN name_search tsvector;
CREATE INDEX idx_name_tsvector ON news USING gin(name_search);
CREATE OR REPLACE FUNCTION update_name_search()
RETURNS trigger AS $$
BEGIN
    NEW.name_search = to_tsvector('english', NEW.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql

CREATE TRIGGER trigger_update_name_search
BEFORE INSERT OR UPDATE OF name ON news
FOR EACH ROW
EXECUTE FUNCTION update_name_search();
```

```bash
git clone https://github.com/Programmer2011bird/space-news-api
cd space-news-api
pip install -r requirements.txt

# Database Configuration
touch database/conf.py
# Edit conf.py with your database credentials
# Running the API
fastapi run API/api.py
# Scraping and inserting news to database
python3 insert_news.py
```

## License  
This project is open-source (MIT License) - See [LICENSE](LICENSE) For details

> [!IMPORTANT]
> This API is intended for **personal, non-commercial use only**. The maintainer is not responsible for misuse of scraped data.
