from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from mrhlab.apis.v1 import api_v1
from mrhlab.models import  Pastebin
from mrhlab.apis.v1.schemas import paste_schema

class IndexAPI(MethodView):

    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://mrhlab.fun/api/v1",
            "paste_url": "http://mrhlab.fun/api/v1/paste/{paste_shortlink}",
        })

class PasteAPI(MethodView):

    def get(self, shorturl):
        """Get item."""
        paste = Pastebin.query.get_or_404(shorturl)
        return jsonify(paste_schema(paste))


api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/paste/<shorturl>', view_func=PasteAPI.as_view('paste'), methods=['GET'])