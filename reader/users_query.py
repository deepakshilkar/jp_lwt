from peewee import *
import sqlite3

db = SqliteDatabase('reader/databases/users_words.db', **{})

class BaseModel(Model):
    class Meta:
        database = db

class Word(BaseModel):
    word_name = CharField(unique=True)

class User(BaseModel):
    username = CharField(unique=True)


class Users_Words(BaseModel):
    username = ForeignKeyField(User, backref='user')
    word_name = ForeignKeyField(Word, backref='word')
    status = IntegerField()

    class Meta:
        indexes = (
            (('user', 'word'), True),
        )


# Get ID for corresponding user
def get_user_id(username):
    query = User.get_or_create(username="moi")
    ident = query[0].id
    return ident


# Returns word ID or creates one if needed
def get_word_id(word):
    query = Word.get_or_create(word_name=word)
    ident = query[0].id
    return ident


# Get dict of key=word value=knowledge_level
def get_knowledge(username):
    db.connect()
    known_words = {}

    query = (Users_Words
             .select()
             .join(Word)
             .where(Users_Words.username == get_user_id(username))
             )

    for t in query:
        known_words[t.word_name.word_name] = t.status

    db.close()

    return known_words


# Add word to user's knowledge base
def add_word(user, word, level):
    db.close()
    db.connect()

    u_id = get_user_id(user)
    w_id = get_word_id(word)

    # Delete row matching the current user/word pair
    delete = Users_Words.delete().where(
        (Users_Words.word_name_id == w_id) &
        (Users_Words.username_id == u_id))
    delete.execute()

    # Insert new pair
    query = Users_Words.insert({'word_name_id': w_id,
                                'username_id': u_id,
                                'status': level})

    query.execute()
    db.close()
