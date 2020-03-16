from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from mrhlab.forms.pastebin import GenerateForm
from mrhlab.extensions import db, mongo, cache
from mrhlab.models import Pastebin


import datetime

bp = Blueprint('pastebin', __name__)


def generate_base62(s):
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def base_encode(num, base=62):
        digits = []
        while num > 0:
            remainder = num%base
            digits.append(BASE62[remainder])
            num = num//base
        return ''.join(digits[::-1])
        
    import hashlib
    md5Val = int(hashlib.md5(s.encode('utf-8')).hexdigest(),base=16)
    hashVal = base_encode(md5Val)
    return hashVal
    

@bp.route('/intro')
def intro():
    return render_template('/pastebin/_intro.html')

@bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    content = data['content'].strip()
    if data is None or content == '':
        return jsonify(message='Invalid content.'), 400

    URL_LENGTH = 7
    datetime_ = datetime.datetime.utcnow()
    seed = request.remote_addr + str(datetime_)
    base62val = generate_base62(seed)[:URL_LENGTH]
    pastebin_ = Pastebin(shortlink=base62val, original=content, created_at=datetime_)
    inserted = False
    while not inserted:
        try:
            db.session.add(pastebin_)
            db.session.commit()
        except:
            datetime_ = datetime.datetime.utcnow()
            seed = request.remote_addr + str(datetime_)
            base62val = generate_base62(seed)[:URL_LENGTH]
            pastebin_ = Pastebin(shortlink=base62val, original=content, created_at=datetime_)
        else:
            inserted = True

    short_URL = base62val
    return render_template('/pastebin/_generate.html', short_URL=short_URL)

@bp.route('/', methods=('GET', 'POST'))
def index():
    form = GenerateForm()
    if request.method == 'POST' and form.validate():
        URL_LENGTH = 7
        datetime_ = datetime.datetime.utcnow()
        seed = request.remote_addr + str(datetime_)
        base62val = generate_base62(seed)[:URL_LENGTH]
        pastebin_= Pastebin(shortlink=base62val, original=form.original.data,  created_at=datetime_)
        inserted = False
        while not inserted:
            try:
                db.session.add(pastebin_)
                db.session.commit()
            except:
                datetime_ = datetime.datetime.utcnow()
                seed = request.remote_addr + str(datetime_)
                base62val = generate_base62(seed)[:URL_LENGTH]
                pastebin_= Pastebin(shortlink=base62val, original=form.original.data, created_at=datetime_)
            else:
                inserted = True
        return form.original.data +' '+base62val
    return render_template('pastebin/index.html', form=form)

@bp.route('/<shorturl>')
@cache.cached(timeout=10*60)
def getpaste(shorturl):
    content = Pastebin.query.get(shorturl).original
    return render_template('pastebin/paste_item.html', content=content)
    
@bp.route('/mongo', methods=('GET', 'POST'))
def indexMongo():
    form = GenerateForm()
    if request.method == 'POST' and form.validate():
        URL_LENGTH = 7
        datetime_ = datetime.datetime.utcnow()
        seed = request.remote_addr + str(datetime_)
        base62val = generate_base62(seed)[:URL_LENGTH]
        paste = {'_id':base62val, 'original':form.original.data, 'created_at':datetime_}
        inserted = False
        pastebin = mongo.db.pastebin
        while not inserted:
            try:
                pastebin.insert_one(paste)
            except:
                datetime_ = datetime.datetime.utcnow()
                seed = request.remote_addr + str(datetime_)
                base62val = generate_base62(seed)[:URL_LENGTH]
                paste = {'_id':base62val, 'original':form.original.data, 'created_at':datetime_}
            else:
                inserted = True
        return form.original.data +' '+base62val
    return render_template('pastebin/index.html', form=form)
    
@bp.route('/mongo/<shorturl>')
def getpasteMongo(shorturl):
    return mongo.db.pastebin.find_one({"_id": shorturl})['original']
