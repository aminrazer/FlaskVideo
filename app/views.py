from app import app, db
from models import video
from models import posting
import os, json, re
from flask import Flask, Response,make_response, jsonify, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from forms import videoUploadForm
from forms import SubtitleForm
from subprocess import call
from werkzeug.contrib.fixers import ProxyFix
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = set(['mp4','mov','webm'])
app.secret_key = 'some_secret'
app.wsgi_app = ProxyFix(app.wsgi_app)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    videos=video.query.order_by('id').all()
    return render_template('indexold.html',videos=videos)

@app.route('/upload', methods=['GET','POST'])
def upload():
	form = videoUploadForm()
	if request.method == 'POST':
		if not form.validate_on_submit():
			print form.errors
			return render_template('upload.html', form=form) 
		if form.validate_on_submit():
			file = request.files['file']
			if file and allowed_file(file.filename):
			    filename = secure_filename(file.filename)
			    ip = request.remote_addr
			    newVideo = video(Title = form.Title.data, Description = form.Description.data, IP =str(ip), location ='/uploads', Views = 0)
			    db.session.add(newVideo)
			    db.session.commit()
		        videoid = str(newVideo.id)
		        videoname = videoid + '.' + filename.rsplit('.', 1)[1]
		        file.save(os.path.join(app.config['UPLOAD_FOLDER'], videoname))
		        call(['/home/amin/bin/ffmpeg', '-i', 'app/static/'+videoname, '-ss', '00:00:02', '-f', 'image2', '-vframes', '1', '-vf', 'scale=320:-1', 'app/static/'+videoid+'.jpeg'])
		        call(['/home/amin/bin/ffmpeg', '-i', 'app/static/'+videoname, '-vcodec', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis', 'app/static/' + videoid + '.webm'])
		        #call(['rm', videoname])
		        dur=os.popen(" /home/amin/bin/ffmpeg -i app/static/"+videoid +".webm 2>&1 | grep Duration: | cut -f2- -d: | cut -f1 -d, | tr -d ' '").readlines()
		        newVideo.Duration=dur[0][0:8]
		        db.session.add(newVideo)
		        db.session.commit()
		        return redirect(url_for('uploaded_file',filename=videoid))
	    
		return render_template('upload.html', form=form,error='no video or not the right format') 
	
	elif request.method == 'GET':
		return render_template('upload.html', form=form) 

@app.route('/v/<filename>')
def uploaded_file(filename):
	if filename.isdigit():
	   video1 = video.query.get(filename)
	   if video1:
			Title=video1.Title
			video1.Views = video1.Views + 1
			Views=video1.Views
			Description=video1.Description
			Duration=video1.Duration
			videoid = filename +'.webm'
			db.session.add(video1)
			db.session.commit()
			return render_template('video.html',Title=Title,videoid=videoid,Views=Views,Description=Description,Duration=Duration) 
	return 'video not found'
def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413
    
@app.route('/test')
def test():
	return render_template('test.html')

