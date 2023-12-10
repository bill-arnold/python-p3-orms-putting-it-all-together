import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')

    def save(self):
        if self.id:
            sql = 'UPDATE dogs SET name=?, breed=? WHERE id=?'
            CURSOR.execute(sql, (self.name, self.breed, self.id))
        else:
            sql = 'INSERT INTO dogs (name, breed) VALUES (?, ?)'
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        if row:
            dog = cls(row[1], row[2])
            dog.id = row[0]
            return dog
        return None

    @classmethod
    def get_all(cls):
        sql = 'SELECT * FROM dogs'
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = 'SELECT * FROM dogs WHERE name=?'
        result = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(result) if result else None

    @classmethod
    def find_by_id(cls, id):
        sql = 'SELECT * FROM dogs WHERE id=?'
        result = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(result) if result else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name_and_breed(name, breed)
        if dog:
            return dog
        else:
            return cls.create(name, breed)

    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        sql = 'SELECT * FROM dogs WHERE name=? AND breed=?'
        result = CURSOR.execute(sql, (name, breed)).fetchone()
        return cls.new_from_db(result) if result else None

    def update(self):
        self.save()