from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3


app = Flask(__name__)
DB_NAME = "reviews.db"
app.json.ensure_ascii = False


class Review:
    TABLE_NAME = "reviews"

    def __init__(self, text, sentiment=None, created_at=None, id_=None):
        self.id = id_
        self.text = text
        self.sentiment = sentiment if sentiment else self.understand_sentiment(text)
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()

    def save(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO {self.TABLE_NAME} (text, sentiment, created_at)
                VALUES (?, ?, ?)
            """,
                (self.text, self.sentiment, self.created_at),
            )
            conn.commit()
            self.id = cursor.lastrowid
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "sentiment": self.sentiment,
            "created_at": self.created_at,
        }

    @classmethod
    def create_table(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )
            conn.commit()

    @classmethod
    def get_reviews(cls, sentiment_filter=None):
        query = f"SELECT id, text, sentiment, created_at FROM {cls.TABLE_NAME}"
        params = ()

        if sentiment_filter:
            query += " WHERE sentiment = ?"
            params = (sentiment_filter,)

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [
            cls(id_=row[0], text=row[1], sentiment=row[2], created_at=row[3])
            for row in rows
        ]

    @staticmethod
    def understand_sentiment(text: str):
        """Статичный метод для определения настроения отзыва. Решил реализовать через 'очки' для обработки случаев,
        когда в отзыве есть как 'хорошие' так и 'плохие' слова.
        В зависимости от того, каких больше, определяется итоговое настроение отзыва"""
        positive_words = ["хорош", "люблю"]
        negative_words = ["плохо", "ненавиж"]
        text = text.lower()
        score = 0

        for word in positive_words:
            score += text.count(word)
        for word in negative_words:
            score -= text.count(word)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        return "neutral"


@app.route("/reviews", methods=["POST"])
def post_reviews():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return (
            jsonify(
                {"error": "Отсутствует переменная 'text'"}
            ),
            400,
        )

    review = Review(text).save()
    return jsonify(review.to_dict()), 201


@app.route("/reviews", methods=["GET"])
def get_reviews():
    sentiment_filter = request.args.get("sentiment")
    reviews = Review.get_reviews(sentiment_filter=sentiment_filter)
    return jsonify([r.to_dict() for r in reviews]), 200


if __name__ == "__main__":
    Review.create_table()
    app.run()
