from flask import Flask, request
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)


class Review:
    """Класс для работы с БД как с ОРМ"""
    def __init__(self, text, sentiment=None, created_at=None, id_=None):
        self.id = id_
        self.text = text
        self.sentiment = sentiment if sentiment else self.understand_sentiment(text)
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()


    def save(self):
        with sqlite3.connect('reviews.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (text, sentiment, created_at)
                VALUES (?, ?, ?)
            ''', (self.text, self.sentiment, self.created_at))
            conn.commit()
            self.id = cursor.lastrowid
        return self


    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "sentiment": self.sentiment,
            "created_at": self.created_at
        }


    @classmethod
    def create_table(cls):
        """Создает таблицу в базе данных, если она не существует, @classmethod для того что бы не было привязки к объекту"""
        with sqlite3.connect('reviews.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()


    @classmethod
    def get_all(cls, sentiment_filter=None):
        """Запрашивает данные из БД с возможностью фильтрации по настроению, @classmethod для того что бы не было привязки к объекту"""
        query = 'SELECT id, text, sentiment, created_at FROM reviews'
        params = ()

        if sentiment_filter:
            query += ' WHERE sentiment = ?'
            params = (sentiment_filter,)

        with sqlite3.connect('reviews.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [
            cls(
                id_=row[0],
                text=row[1],
                sentiment=row[2],
                created_at=row[3]
            ) for row in rows
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


@app.route('/reviews', methods=['POST'])
def post_reviews():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return json.dumps({"error": "Отсутствует переменная 'text'"}, indent=4, ensure_ascii=False), 400

    review = Review(text).save()
    return json.dumps(review.to_dict(), indent=4, ensure_ascii=False), 201


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment_filter = request.args.get('sentiment')
    reviews = Review.get_all(sentiment_filter=sentiment_filter)
    return json.dumps([r.to_dict() for r in reviews], indent=4, ensure_ascii=False), 200


if __name__ == '__main__':
    Review.create_table()
    app.run()
