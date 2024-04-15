import random  # Импорт модуля для генерации случайных чисел
from flask import Flask, render_template  # Импорт Flask и функции для рендеринга HTML-шаблонов
from faker import Faker  # Импорт Faker для генерации фальшивых данных

fake = Faker()  # Создание экземпляра Faker для генерации данных

app = Flask(__name__)  # Создание экземпляра Flask приложения
application = app  # Присваивание Flask приложения переменной application (часто используется в WSGI серверах)

# Список UUID для использования в качестве идентификаторов изображений постов
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):  # Функция для генерации комментариев с возможностью рекурсивных ответов
    comments = []  # Пустой список для комментариев
    for i in range(random.randint(1, 3)):  # Генерация от 1 до 3 комментариев
        comment = {'author': fake.name(), 'text': fake.text()}  # Создание комментария с фальшивым автором и текстом
        if replies:  # Если разрешены ответы
            comment['replies'] = generate_comments(replies=False)  # Рекурсивно генерируем ответы без дальнейших ответов
        comments.append(comment)  # Добавление комментария в список
    return comments  # Возвращение списка комментариев

def generate_post(i):  # Функция для генерации поста
    return {
        'title': 'Заголовок поста',  # Статический заголовок поста
        'text': fake.paragraph(nb_sentences=100),  # Генерация абзаца из 100 предложений
        'author': fake.name(),  # Генерация фальшивого имени автора
        'date': fake.date_time_between(start_date='-2y', end_date='now'),  # Генерация даты поста в промежутке последних двух лет
        'image_id': f'{images_ids[i]}.jpg',  # Присваивание изображения посту
        'comments': generate_comments()  # Генерация комментариев для поста
    }

# Создание списка постов, сортированных по дате в обратном порядке
posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')  # Маршрут к корневой странице
def index():  # Функция обработчик для корневой страницы
    return render_template('index.html')  # Рендеринг шаблона для главной страницы

@app.route('/posts')  # Маршрут к странице с постами
def posts():  # Функция обработчик для страницы с постами
    return render_template('posts.html', title='Посты', posts=posts_list)  # Рендеринг шаблона страницы постов с передачей списка постов

@app.route('/posts/<int:index>')  # Маршрут к конкретному посту, с указанием индекса поста
def post(index):  # Функция обработчик для страницы конкретного поста
    p = posts_list[index]  # Получение поста по индексу
    return render_template('post.html', title=p['title'], post=p)  # Рендеринг шаблона поста с передачей данных поста

@app.route('/about')  # Маршрут к странице "Об авторе"
def about():  # Функция обработчик для страницы "Об авторе"
    return render_template('about.html', title='Об авторе')  # Рендеринг шаблона страницы "Об авторе"

if __name__ == '__main__':  # Проверка, является ли скрипт главным модулем
    app.run(debug=True)  # Запуск приложения в режиме отладки
