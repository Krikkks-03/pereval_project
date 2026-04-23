import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class PerevalDatabase:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Устанавливает соединение с БД"""
        self.conn = psycopg2.connect(
            host=os.getenv("FSTR_DB_HOST"),
            port=os.getenv("FSTR_DB_PORT"),
            user=os.getenv("FSTR_DB_LOGIN"),
            password=os.getenv("FSTR_DB_PASS"),
            database=os.getenv("FSTR_DB_NAME", "pereval"),
            cursor_factory=RealDictCursor
        )
        return self.conn

    def close(self):
        """Закрывает соединение"""
        if self.conn:
            self.conn.close()

    def get_or_create_user(self, user_data: dict) -> int:
        """
        Возвращает ID пользователя.
        Если пользователя с таким email нет — создаёт.
        """
        cursor = self.conn.cursor()

        # Пытаемся найти пользователя по email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data["email"],))
        user = cursor.fetchone()

        if user:
            return user["id"]

        # Создаём нового пользователя
        cursor.execute("""
            INSERT INTO users (email, phone, fam, name, otc)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            user_data["email"],
            user_data["phone"],
            user_data["fam"],
            user_data["name"],
            user_data.get("otc", "")
        ))
        return cursor.fetchone()["id"]

    def add_coords(self, coords_data: dict) -> int:
        """Добавляет координаты и возвращает их ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO coords (latitude, longitude, height)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (
            coords_data["latitude"],
            coords_data["longitude"],
            coords_data["height"]
        ))
        return cursor.fetchone()["id"]

    def add_pereval(self, pereval_data: dict) -> int:
        """
        Добавляет новый перевал.
        Возвращает ID созданной записи.
        """
        cursor = self.conn.cursor()

        # 1. Пользователь
        user_id = self.get_or_create_user(pereval_data["user"])

        # 2. Координаты
        coords_id = self.add_coords(pereval_data["coords"])

        # 3. Добавляем перевал
        cursor.execute("""
            INSERT INTO pereval (
                beauty_title, title, other_titles, connect, add_time,
                user_id, coords_id,
                level_winter, level_summer, level_autumn, level_spring,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            pereval_data["beauty_title"],
            pereval_data["title"],
            pereval_data.get("other_titles", ""),
            pereval_data.get("connect", ""),
            pereval_data["add_time"],
            user_id,
            coords_id,
            pereval_data["level"].get("winter", ""),
            pereval_data["level"].get("summer", ""),
            pereval_data["level"].get("autumn", ""),
            pereval_data["level"].get("spring", ""),
            "new"
        ))
        pereval_id = cursor.fetchone()["id"]

        # 4. Добавляем изображения
        for img in pereval_data["images"]:
            cursor.execute("""
                INSERT INTO pereval_images (pereval_id, title, img_data)
                VALUES (%s, %s, %s)
            """, (pereval_id, img["title"], img.get("data", "")))

        self.conn.commit()
        return pereval_id