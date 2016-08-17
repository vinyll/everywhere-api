import os

from tinydb import TinyDB, where, Query
from xkcdpass import xkcd_password as xp


db = {'users': None, 'contents': {}}


class DuplicateException(Exception):
    pass


def init(config):
    path = config['STORAGE_PATH']
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    db['users'] = TinyDB(os.path.join(path, 'users.json'))
    db['content_parser'] = TinyDB(os.path.join(path, 'contents.json'))


def get_owner(name):
    Owner = Query()
    return db['users'].get(Owner.name == name)


def create_owner(name):
    Owner = Query()
    # No duplicate
    if db['users'].get(Owner.name == name):
        raise DuplicateException

    wordfile = xp.locate_wordfile()
    words = xp.generate_wordlist(wordfile=wordfile, min_length=3, max_length=8)
    user_id = db['users'].insert({
        'name': name,
        'key': xp.generate_xkcdpassword(words, numwords=4)
    })
    return db['users'].get(eid=user_id)


def owner_to_id(owner):
    '''Allow `owner` argument to be an id or an Owner object.'''
    owner_id = owner
    if hasattr(owner, 'eid'):
        owner_id = owner.eid
    return owner_id


def get_content(name, owner):
    owner_id = owner_to_id(owner)
    Content = Query()
    return db['content_parser'].get((Content.name == name) &
                           (Content.owner == owner_id))


def create_content(name, value, owner):
    owner_id = owner_to_id(owner)
    Content = Query()

    if get_content(name, owner):
        raise DuplicateException

    content_id = db['content_parser'].insert({
        'name': name,
        'value': value,
        'owner': owner_id
    })
    return get_content(name, owner)


def update_content(name, value, owner):
    Content = Query()
    content = get_content(name, owner)
    content_id = db['content_parser'].update({'value': value}, eids=[content.eid])[0]
    return get_content(name, owner)


def crupdate_content(name, value, owner):
    method = update_content if get_content(name, owner) else create_content
    return method(name, value, owner)


def drop_all():
    db['users'].purge_tables()
    db['content_parser'].purge_tables()
