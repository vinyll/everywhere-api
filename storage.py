import os

from tinydb import TinyDB, where, Query
from xkcdpass import xkcd_password as xp


class DuplicateException(Exception):
    pass


def get_owner(name, key):
    Owner = Query()
    return users_db.get((Owner.name == name) & (Owner.key == key))


def create_owner(name):
    Owner = Query()
    # No duplicate
    if users_db.get(Owner.name == name):
        raise DuplicateException

    wordfile = xp.locate_wordfile()
    words = xp.generate_wordlist(wordfile=wordfile, min_length=3, max_length=8)
    user_id = users_db.insert({
        'name': name,
        'key': xp.generate_xkcdpassword(words, numwords=4)
    })
    return users_db.get(eid=user_id)


def owner_to_id(owner):
    '''Allow `owner` argument to be an id or an Owner object.'''
    owner_id = owner
    if hasattr(owner, 'eid'):
        owner_id = owner.eid
    return owner_id


def get_content(name, owner):
    owner_id = owner_to_id(owner)
    Content = Query()
    return contents_db.get((Content.name == name) &
                           (Content.owner == owner_id))


def create_content(name, value, owner):
    owner_id = owner_to_id(owner)
    Content = Query()

    if get_content(name, owner):
        raise DuplicateException

    content_id = contents_db.insert({
        'name': name,
        'value': value,
        'owner': owner_id
    })
    return get_content(name, owner)


def update_content(name, value, owner):
    Content = Query()
    content = get_content(name, owner)
    content_id = contents_db.update({'value': value}, eids=[content.eid])[0]
    return get_content(name, owner)


def crupdate_content(name, value, owner):
    method = update_content if get_content(name, owner) else create_content
    return method(name, value, owner)


def prepare(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    return (TinyDB(os.path.join(path, 'users.json')),
            TinyDB(os.path.join(path, 'contents.json')))


def drop_all():
    users_db.purge_tables()
    contents_db.purge_tables()


(users_db, contents_db) = prepare('data/')
