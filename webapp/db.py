import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "xs_and_os"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password")
    )


def create_user(username, plain_password):
    hashed = generate_password_hash(plain_password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO app_user (username, password_hash) VALUES (%s, %s) RETURNING user_id",
        (username, hashed)
    )
    new_user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return new_user_id


def check_login(username, plain_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, password_hash FROM app_user WHERE username = %s",
        (username,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return None

    user_id, stored_hash = row
    if check_password_hash(stored_hash, plain_password):
        return user_id
    return None


def record_game(user_id, result, seconds_taken):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO game (user_id, result, seconds_taken) VALUES (%s, %s, %s)",
        (user_id, result, seconds_taken)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_stats_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM game WHERE user_id = %s", (user_id,))
    games_played = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(seconds_taken) FROM game WHERE user_id = %s", (user_id,))
    average_seconds = cursor.fetchone()[0]

    cursor.execute(
        "SELECT MAX(seconds_taken), MIN(seconds_taken) FROM game WHERE user_id = %s AND result = 'WIN'",
        (user_id,)
    )
    longest_win, shortest_win = cursor.fetchone()

    cursor.execute(
        "SELECT MAX(seconds_taken), MIN(seconds_taken) FROM game WHERE user_id = %s AND result = 'LOSS'",
        (user_id,)
    )
    longest_loss, shortest_loss = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "games_played": games_played,
        "average_seconds": average_seconds,
        "longest_win": longest_win,
        "shortest_win": shortest_win,
        "longest_loss": longest_loss,
        "shortest_loss": shortest_loss
    }