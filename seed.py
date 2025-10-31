from app import app, db
from models import Role, User, Genre, Cover, Book, BookGenre, Review, Visit
from datetime import datetime, timedelta
import hashlib
import os

def seed_database():
    """Заполняет БД начальными данными"""
    with app.app_context():
        # Очищаем все таблицы
        db.drop_all()
        db.create_all()
        
        print("📚 Начинаем заполнение БД...")
        
        # 1. Создаём роли
        print("\n1️⃣ Создание ролей...")
        admin_role = Role(id=1, name='admin', description='Администратор')
        moder_role = Role(id=2, name='moderator', description='Модератор')
        user_role = Role(id=3, name='user', description='Обычный пользователь')
        db.session.add_all([admin_role, moder_role, user_role])
        db.session.commit()
        print("✓ Роли созданы")
        
        # 2. Создаём пользователей
        print("\n2️⃣ Создание пользователей...")
        admin = User(
            login='admin',
            last_name='Админов',
            first_name='Админ',
            middle_name='Админович',
            role_id=1
        )
        admin.set_password('admin123')
        
        moder = User(
            login='moderator',
            last_name='Модеров',
            first_name='Модер',
            middle_name='Модерович',
            role_id=2
        )
        moder.set_password('moder123')
        
        user1 = User(
            login='ivan',
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович',
            role_id=3
        )
        user1.set_password('ivan123')
        
        user2 = User(
            login='maria',
            last_name='Петрова',
            first_name='Мария',
            middle_name='Петровна',
            role_id=3
        )
        user2.set_password('maria123')
        
        db.session.add_all([admin, moder, user1, user2])
        db.session.commit()
        print("✓ Пользователи созданы")
        
        # 3. Создаём жанры
        print("\n3️⃣ Создание жанров...")
        genres_data = ['Фантастика', 'Приключения', 'Детектив', 'Романтика', 'Ужас', 'Драма']
        genres = []
        for name in genres_data:
            genre = Genre(name=name)
            genres.append(genre)
            db.session.add(genre)
        db.session.commit()
        print(f"✓ {len(genres)} жанров создано")
        
        # 4. Создаём обложки для Harry Potter
        print("\n4️⃣ Создание обложек...")
        cover_files = [
            ('23_22_Harry_Potter_and_the_Philosophers_Stone.jpg', 'Философский камень'),
            ('16_Harry_Potter_and_the_Chamber_of_Secrets.jpg', 'Тайная комната'),
            ('7Harry_Potter_and_the_Prisoner_of_Azkaban.jpg', 'Узник Азкабана'),
            ('12_Harry_Potter_and_the_Goblet_of_Fire.jpg', 'Кубок огня'),
            ('5Harry_Potter_and_the_Order_of_the_Phoenix.jpg', 'Орден Феникса'),
            ('11_10_Harry_Potter_and_the_Half-Blood_Prince.jpg', 'Принц-полукровка'),
            ('2Harry_Potter_and_the_Deathly_Hallows.jpg', 'Дары Смерти'),
        ]
        
        covers = []
        for filename, title in cover_files:
            # Вычисляем MD5 хеш для имитации
            md5_hash = hashlib.md5(title.encode()).hexdigest()
            cover = Cover(
                file_name=filename,
                mime_type='image/jpg',
                md5_hash=md5_hash
            )
            covers.append(cover)
            db.session.add(cover)
        db.session.commit()
        print(f"✓ {len(covers)} обложек создано")
        
        # 5. Создаём книги
        print("\n5️⃣ Создание книг...")
        books_data = [
            {
                'title': 'Гарри Поттер и философский камень',
                'author': 'Джоан Роулинг',
                'year': 1997,
                'publisher': 'Bloomsbury',
                'pages': 223,
                'description': 'Первая книга о молодом волшебнике Гарри Поттере, который узнает о своих магических способностях и поступает в школу волшебства Хогвартс.',
                'genres': [0],
                'cover_id': 1
            },
            {
                'title': 'Гарри Поттер и тайная комната',
                'author': 'Джоан Роулинг',
                'year': 1998,
                'publisher': 'Bloomsbury',
                'pages': 251,
                'description': 'Вторая книга серии. Во время второго года в Хогвартсе начинают исчезать студенты после атак таинственного монстра.',
                'genres': [0, 1],
                'cover_id': 2
            },
            {
                'title': 'Гарри Поттер и узник Азкабана',
                'author': 'Джоан Роулинг',
                'year': 1999,
                'publisher': 'Bloomsbury',
                'pages': 317,
                'description': 'Третья книга серии. Из волшебной тюрьмы Азкабана бежит опасный преступник Сириус Блэк.',
                'genres': [0, 1, 2],
                'cover_id': 3
            },
            {
                'title': 'Гарри Поттер и кубок огня',
                'author': 'Джоан Роулинг',
                'year': 2000,
                'publisher': 'Bloomsbury',
                'pages': 636,
                'description': 'Четвёртая книга серии. Гарри неожиданно выбран участником опасного Турнира Трёх Волшебников.',
                'genres': [0, 1],
                'cover_id': 4
            },
            {
                'title': 'Гарри Поттер и Орден Феникса',
                'author': 'Джоан Роулинг',
                'year': 2003,
                'publisher': 'Bloomsbury',
                'pages': 766,
                'description': 'Пятая книга серии. Гарри и его друзья готовятся к возвращению Вольдеморта.',
                'genres': [0, 5],
                'cover_id': 5
            },
            {
                'title': 'Гарри Поттер и Принц-полукровка',
                'author': 'Джоан Роулинг',
                'year': 2005,
                'publisher': 'Bloomsbury',
                'pages': 607,
                'description': 'Шестая книга серии. Гарри узнаёт о способе сделать Вольдеморта бессмертным.',
                'genres': [0, 5],
                'cover_id': 6
            },
            {
                'title': 'Гарри Поттер и Дары Смерти',
                'author': 'Джоан Роулинг',
                'year': 2007,
                'publisher': 'Bloomsbury',
                'pages': 759,
                'description': 'Седьмая и завершающая книга серии. Финальная битва между Гарри и Вольдемортом.',
                'genres': [0, 1, 5],
                'cover_id': 7
            },
            
        ]
        
        books = []
        for book_data in books_data:
            genres_list = book_data.pop('genres')
            book = Book(**book_data)
            books.append(book)
            db.session.add(book)
            db.session.flush()
            
            # Связываем с жанрами
            for genre_id in genres_list:
                bg = BookGenre(book_id=book.id, genre_id=genres[genre_id].id)
                db.session.add(bg)
        
        db.session.commit()
        print(f"✓ {len(books)} книг создано")
        
        # 6. Создаём рецензии
        print("\n6️⃣ Создание рецензий...")
        reviews = [
            Review(book_id=1, user_id=1, rating=5, text='Отличная книга! Захватывающий сюжет и интересные персонажи.'),
            Review(book_id=1, user_id=2, rating=4, text='Хорошее начало серии. Нравятся описания мира магии.'),
            Review(book_id=2, user_id=1, rating=5, text='Ещё лучше, чем первая! Тайна комнаты была интересной.'),
            Review(book_id=3, user_id=3, rating=4, text='Понравилась история про Сириуса.'),
            Review(book_id=4, user_id=2, rating=5, text='Турнир был очень напряжённым. Лучшая книга в серии!'),
            Review(book_id=5, user_id=1, rating=3, text='Начало было медленным, но конец компенсировал.'),
            Review(book_id=7, user_id=2, rating=5, text='Отличное завершение серии. Эмоциональный конец.'),
            Review(book_id=8, user_id=1, rating=5, text='Классический роман-антиутопия. Остаётся актуальным.'),
        ]
        db.session.add_all(reviews)
        db.session.commit()
        print(f"✓ {len(reviews)} рецензий создано")
        
        # 7. Создаём посещения
        print("\n7️⃣ Создание посещений...")
        visits = []
        now = datetime.utcnow()
        
        # Создаём посещения за последние 90 дней
        for i in range(20):
            visit = Visit(
                user_id=None if i % 3 == 0 else (i % 4 + 1),  # Часть анонимных
                book_id=(i % len(books)) + 1,
                visit_time=now - timedelta(days=i % 89)
            )
            visits.append(visit)
            db.session.add(visit)
        
        db.session.commit()
        print(f"✓ {len(visits)} посещений создано")
        
        print("\n" + "="*50)
        print("✅ БД успешно заполнена!")
        print("="*50)
        print("\nДанные для входа:")
        print("━" * 50)
        print("👨‍💼 Администратор:")
        print("   Логин: admin")
        print("   Пароль: admin123")
        print("━" * 50)
        print("👮 Модератор:")
        print("   Логин: moderator")
        print("   Пароль: moder123")
        print("━" * 50)
        print("👤 Пользователь 1:")
        print("   Логин: ivan")
        print("   Пароль: ivan123")
        print("━" * 50)
        print("👤 Пользователь 2:")
        print("   Логин: maria")
        print("   Пароль: maria123")
        print("━" * 50)

if __name__ == '__main__':
    seed_database()