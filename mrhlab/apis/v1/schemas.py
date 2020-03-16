from flask import url_for

def paste_schema(paste):
    return {
        'shortlink': paste.shortlink,
        'self': url_for('pastebin.getpaste', shorturl=paste.shortlink, _external=True),
        'kind': 'Paste',
        'content': paste.original,
        'createtime':paste.created_at
    }