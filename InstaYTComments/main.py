import os
import re
from werkzeug import secure_filename
from flask import Flask, render_template, request, url_for, current_app
from services.ngram import run as runGRAM
from services.tfidf import run as runIDF
from services.sent_analysis import run as runSentiment
from services.wordcloud import run as runWordCloud
from services.scraping import read_file, yt_scrap, insta_scrap

app = Flask("nlp")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')

@app.route("/", methods=['GET'])
def begin():
    return render_template('first.html', logo_url='/static/img/logo.png')


@app.route("/youtube", methods=['GET'])
def youtube():
    return render_template('scraping.html', logo_url='/static/img/logo.png', action='/youtube', 
                           first_input='Enter YouTube link: ', obs='* Interation is the number of times the page will scroll down to load new comments (each interation give about 20 comments).')

@app.route("/youtube", methods=['POST'])
def show_yt():
    n = request.form['number']
    url = request.form['url']
    lang = request.form['lang']

    if not n.isdigit():
        return render_template('error.html', logo_url='/static/img/logo.png',err=f'The number {n} is WRONG!!!', 
                                err_description=f'Please select a positive integer and try again.', 
                                go_back=url_for('youtube'))
    else:
        n = int(n) + 1
        
    if not re.search('^https://www.youtube.com/|^http://www.youtube.com/|^www.youtube.com/|^youtube.com/', url):
        return render_template('error.html', logo_url='/static/img/logo.png',err=f'The URL is WRONG!!!', 
                                err_description='It should follow the following format: https://www.youtube.com/watch?v=goMp OR http://www.youtube.com/watch?v=goMp OR www.youtube.com/watch?v=goMp OR youtube.com/watch?v=goMp.', 
                                go_back=url_for('youtube'))
    if re.search('^www.youtube.com/', url):
        url = 'https://' + url
    if re.search('^youtube.com/', url):
        url = 'https://www.' + url

    lista_commen = yt_scrap(url,n)
    runGRAM(lista_commen, lang)
    dic_sentiment = runSentiment(lista_commen, lang)
    cloud_path = runWordCloud(lista_commen)
    dic_tf_idf = runIDF(lista_commen, lang)
    dic_tf_idf['size'] = range(len(dic_tf_idf['Token']))

    return render_template('info.html', logo_url='/static/img/logo.png', tf_idf=dic_tf_idf, 
                           sentiment=dic_sentiment, wordcloud_path=cloud_path)


@app.route("/insta", methods=['GET'])
def insta():
    return render_template('scraping.html', logo_url='/static/img/logo.png', action='/insta', 
                           first_input='Enter Instagram Post link: ', 
                           obs='* Interation is the number of times the button + will be click to load new comments.')

@app.route("/insta", methods=['POST'])
def show_insta():
    n = request.form['number']
    url = request.form['url']
    lang = request.form['lang']

    if not n.isdigit():
        return render_template('error.html', logo_url='/static/img/logo.png',err=f'The number {n} is WRONG!!!', 
                                err_description=f'Please select a positive integer and try again.', 
                                go_back=url_for('insta'))
    else:
        n = int(n)

    if not re.search('^https://www.instagram.com/|^http://www.instagram.com/|^www.instagram.com/|^instagram.com/', url):
        return render_template('error.html', logo_url='/static/img/logo.png',err=f'The URL is WRONG!!!', 
                                err_description='It should follow the following format: https://www.instagram.com/p/B9POVGJ2Vy/ OR http://www.instagram.com/p/B9POVGJ2Vy/ OR www.instagram.com/p/B9POVGJ2Vy/ OR instagram.com/p/B9POVGJ2Vy/.', 
                                go_back=url_for('insta'))
    if re.search('^www.instagram.com/', url):
        url = 'https://' + url
    if re.search('^instagram.com/', url):
        url = 'https://www.' + url

    lista_commen = insta_scrap(url,n)
    runGRAM(lista_commen, lang)
    dic_sentiment = runSentiment(lista_commen, lang)
    cloud_path = runWordCloud(lista_commen)
    dic_tf_idf = runIDF(lista_commen, lang)
    dic_tf_idf['size'] = range(len(dic_tf_idf['Token']))

    return render_template('info.html', logo_url='/static/img/logo.png', tf_idf=dic_tf_idf, 
                           sentiment=dic_sentiment, wordcloud_path=cloud_path)


@app.route("/upload", methods=['GET'])
def upload():
    return render_template('upload.html', logo_url='/static/img/logo.png')

@app.route("/upload", methods=['POST'])
def show_upload():
    file_info = request.files.get('text')
    lang = request.form['lang']

    if file_info:
        filename = secure_filename(file_info.filename)
        if filename[-4:] != '.txt':
            return render_template('error.html', logo_url='/static/img/logo.png',err=f'The extension {filename[-4:]} is WRONG!!!', 
                                   err_description='Please double check the file extension. We only accept files with extension .txt',
                                   go_back=url_for('upload'))
        path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
        file_info.save(path)
    else:
        return render_template('error.html', logo_url='/static/img/logo.png',err=f'File {filename[:-4]} was not found!!!', 
                                err_description='Please check the file again and try again.', go_back=url_for('upload'))
    
    file_path = current_app.config['MEDIA_ROOT']+'/'+filename
    lista_commen = read_file(file_path)
    runGRAM(lista_commen,lang)
    dic_sentiment = runSentiment(lista_commen, lang)
    cloud_path = runWordCloud(lista_commen)
    dic_tf_idf = runIDF(lista_commen,lang)
    dic_tf_idf['size'] = range(len(dic_tf_idf['Token']))

    return render_template('info.html', logo_url='/static/img/logo.png', tf_idf=dic_tf_idf, 
                           sentiment=dic_sentiment, wordcloud_path=cloud_path)


@app.route("/default", methods=['GET'])
def default():
    file_path = current_app.config['MEDIA_ROOT']+'/default.txt'
    lista_commen = read_file(file_path)

    dic_tf_idf = runIDF(lista_commen,"0")
    dic_tf_idf['size'] = range(len(dic_tf_idf['Token']))
    runGRAM(lista_commen,lang)
    cloud_path = runWordCloud(lista_commen)

    return render_template('info_default.html', logo_url='/static/img/logo.png', 
                           tf_idf=dic_tf_idf, wordcloud_path=cloud_path)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)