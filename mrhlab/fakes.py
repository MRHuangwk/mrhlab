from faker import Faker
from flask import url_for

from mrhlab.models import Admin, Category, Application
from mrhlab.extensions import db
from mrhlab.blueprints import pastebin, styletransfer

fake = Faker()

def fake_admin():
    admin = Admin(
        username='admin',
        lab_title='MR.H LAB',
        lab_sub_title='Never stop exploring.',
        name='MR.H',
        about='Personal Lab of MR.H'
    )
    admin.set_password('fakeadmin')
    db.session.add(admin)
    db.session.commit()

def fake_categories():
    for category_ in ['Default', 'Tool', 'Machine Learning']:
        category = Category(name=category_)
        db.session.add(category)
    try:
        db.session.commit()
    except:
        db.session.rollback()

def fake_applications():
    application = Application(
        name='Paste bin',
        describe='Paste something in it, the we will generate a short-url of it for you to share.',
        screenshot_path='image/pastebin.jpg',
        url='pastebin',
        category_id=2
    )
    db.session.add(application)
    application = Application(
        name='Style Transfer',
        describe='Repaint your photo with famous picture.',
        screenshot_path='image/styletransfer.png',
        url='styletransfer',
        category_id=3
    )
    db.session.add(application)
    db.session.commit()

