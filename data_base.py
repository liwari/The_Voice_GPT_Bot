import sqlite3
from config import DB_FILE
from log import log_info, log_error

path_to_db = DB_FILE


def create_database():
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                role TEXT,
                gpt_tokens INTEGER,
                tts_symbols INTEGER,
                stt_blocks INTEGER)
            ''')
            log_info("DATABASE: База данных создана")
    except Exception as e:
        log_error(e)
        return None


def add_message(user_id, full_message):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            message, role, gpt_tokens, tts_symbols, stt_blocks = full_message
            cursor.execute('''
                    INSERT INTO messages (user_id, message, role, gpt_tokens, tts_symbols, stt_blocks) 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                           (user_id, message, role, gpt_tokens, tts_symbols, stt_blocks))
            conn.commit()
            # log_info(f"DATABASE: INSERT INTO messages "
            #          f"VALUES ({user_id}, {message}, {role}, {gpt_tokens}, {tts_symbols}, {stt_blocks})")
    except Exception as e:
        log_error(e)
        return None


def count_users_without_one_user(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(DISTINCT user_id) FROM messages WHERE user_id <> ?''', (user_id,))
            count = cursor.fetchone()[0]
            return count
    except Exception as e:
        log_error(e)
        return None


def select_n_last_messages(user_id, n_last_messages=10000):
    messages = []
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT message, role, gpt_tokens FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?''',
                           (user_id, n_last_messages))
            data = cursor.fetchall()
            if data and data[0]:
                for message in reversed(data):
                    messages.append({'text': message[0], 'role': message[1]})
            return messages
    except Exception as e:
        log_error(e)
        return messages


def count_all_limits(user_id, limit_type):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT SUM({limit_type}) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                log_info(f"DATABASE: У user_id={user_id} использовано {data[0]} {limit_type}")
                return data[0]
            else:
                return 0
    except Exception as e:
        log_error(e)
        return 0
