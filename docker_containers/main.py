import json

from fastapi import FastAPI, Query
import uvicorn
import psycopg2


DB_PARAMS = {
    "dbname": "****",
    "user": "****",
    "password": "****",  
    "host": "****",
    "port": "5432"
}


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        return conn, cur
    except Exception as e:
        return None, None


def save_to_db(data):
    try:
        conn, cur = connect_to_db()
        if conn is None or cur is None:
            return {"status": "error", "message": "Failed to connect to DB"}
        
        for link in data:
            cur.execute(
                """
                INSERT INTO links (link) VALUES (%s)
                ON CONFLICT (link) DO NOTHING;
                """,
                (link,)
            )

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success", "message": "Data saved"}

    except Exception as e:
        print(f"Exception in save_to_db: {e}")
        return {"status": "error", "message": str(e)}

def get_data_from_db():
    try:
        conn, cur = connect_to_db()
        if conn is None or cur is None:
            return {"status": "error", "message": "Failed to connect to DB"}
        
        cur.execute("SELECT link FROM links;")  
        rows = cur.fetchall()
        
        conn.close()
        
        data = [row[0] for row in rows]
        
        with open("links.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        return {"status": "success", "links": data}
    
    except Exception as e:
        print(f"Exception in get_data_from_db: {e}")
        return {"status": "error", "message": str(e)}

arr = ["google.com", "mail.google.com", "yandex.com", "youtube.com", "mail.com", "apple.com", "logitech.com", "habr.com", "github.com", "stackoverflow.com"]

app = FastAPI()
@app.get("/pull_data")
def pull_data():
    return save_to_db(arr)

@app.get("/get_data")
def get_data():
    return get_data_from_db()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)