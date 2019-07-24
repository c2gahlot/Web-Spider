from flask import render_template, current_app, jsonify
from urllib.parse import urlparse
from .forms import CrawlUrlForm
from ..models import Link
from app import celery
from . import home
from .. import db
import requests
import datetime
import re


def change_url_to_parsed_db(url):
    try:
        link = Link.query.filter_by(url=url).first()
        if link is not None:
            link.status = 'parsed'
            link.parsed_at = datetime.datetime.utcnow()
            db.session.commit()
    except Exception as e:
        print(e)


def not_in_db(url):
    try:
        link = Link.query.filter_by(url=url).first()
        if link is None:
            return True
    except Exception as e:
        print(e)


def save_url_to_db(url):
    try:
        link = Link(url=url)
        # add link to the database
        db.session.add(link)
        db.session.commit()
    except Exception as e:
        print(e)


def crawl_url(url):
    request = requests.get(url, verify=False)
    return request.text.encode('utf-8')


def parse(html, base_url):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      html.decode('utf-8'))
    return [url for url in urls if base_url in url]


@celery.task
def get_urls(url):
    try:
        if not_in_db(url):
            with current_app.app_context():
                save_url_to_db(url)
                html = crawl_url(url)

                url_object = urlparse(url)
                base_url = url_object.scheme + '://' + url_object.netloc
                urls = parse(html, base_url)
                for url in urls:
                    get_urls.apply_async(args=[url])
                change_url_to_parsed_db(url)

    except Exception as exception:
        print(exception)


@home.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Render the homepage template on the / route
    """
    form = CrawlUrlForm()
    if form.validate_on_submit():
        link = form.url.data
        get_urls.apply_async(args=[link])
        return render_template('home/dashboard.html', title="Dashboard")
    return render_template('home/index.html', form=form, title="Welcome")


@home.route('/data')
def get_links_data():
    links = []
    result = Link.query.all()
    for i in result:
        links.append({
            'id': i.id,
            'url': i.url,
            'status': i.status,
            'parsed_at': str(i.parsed_at),
            'created_at': str(i.created_at)
        })
    return jsonify({'data': links})
