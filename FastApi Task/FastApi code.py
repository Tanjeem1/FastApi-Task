from fastapi import FastAPI, HTTPException
import mysql.connector
import bcrypt

app = FastAPI()
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'simple_user_registration'
}
def get_db():
    return mysql.connector.connect(**db_config)

@app.post("/register/")
async def register_user(username: str, password: str, country: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        db.close()
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute(
        "INSERT INTO users (username, password, country) VALUES (%s, %s, %s)",
        (username, hashed_password, country)
    )
    db.commit()
    cursor.close()
    db.close()
    return {"message": f"User {username} registered successfully!"}
