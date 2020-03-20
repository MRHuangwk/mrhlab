import os

from flask import Blueprint, render_template, request, flash, url_for, redirect, send_from_directory, current_app
from flask_login import login_required, current_user
from mrhlab.forms.styletranfer import TransferForm
from mrhlab.utils import rename_image, resize_image
from mrhlab.models import Transfer
from mrhlab.extensions import db
from mrhlab import style_transfer_task

bp = Blueprint('styletransfer', __name__)


@bp.route('/')
def index():
    return render_template('styletransfer/index.html')


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = TransferForm()
    if request.method == 'POST':
        if form.validate():
            f = form.photo.data
            print(f)
            if f:
                filename = rename_image(f.filename)
                path = os.path.join(current_app.config['UPLOAD_CONTENT_PATH'], filename)
                f.save(path)
                filename = resize_image(f, filename, current_app.config['CONTENT_PHOTO_SIZE'])
            else:
                filename = 'shanghai.jpg'
            styleFilename = form.style.data + '.jpg'
            transfer = Transfer(
                style=styleFilename,
                content=filename,
                user=current_user._get_current_object(),
                result = styleFilename.split('.')[0]+filename.split('.')[0]+'.png'
            )
            db.session.add(transfer)
            db.session.commit()
            style_transfer_task.delay(contentfilename=filename, stylefilename=styleFilename)

            return redirect(url_for('.result'))
    return render_template('styletransfer/upload.html', form=form)

@bp.route('/result', methods=('GET', 'POST'))
@login_required
def result():
    transfers = Transfer.query.filter_by(user=current_user._get_current_object()).order_by(Transfer.id.desc()).all()
    return render_template('styletransfer/result.html', transfers=transfers)


@bp.route('/uploads/content/<path:filename>')
def get_content_image(filename):
    return send_from_directory(current_app.config['UPLOAD_CONTENT_PATH'], filename)


@bp.route('/uploads/style/<path:filename>')
def get_style_image(filename):
    return send_from_directory(current_app.config['UPLOAD_STYLE_PATH'], filename)


@bp.route('/uploads/result/<path:filename>')
def get_result_image(filename):
    return send_from_directory(current_app.config['UPLOAD_RESULT_PATH'], filename)