from flask import render_template, session
from urllib.parse import urlparse
from .forms import CrawlUrlForm
from datetime import timedelta
from ..models import Link
from app import celery
from . import home
from .. import db
import traceback
import requests
import re


def not_in_db(url):
    try:
        link = Link.query.filter_by(url=url).first()

        if link is None:
            return True

    except Exception as err:
        try:
            raise TypeError("Again !?!")
        except:
            pass
        traceback.print_exc()
    return False


def save_url_to_db(session_id, url):
    try:
        link = Link(session_id=session_id,
                    url=url)

        # add link to the database
        db.session.add(link)
        db.session.commit()

    except Exception as err:
        try:
            raise TypeError("Again !?!")
        except:
            pass

        traceback.print_exc()

def crawl_url(url):
    request = requests.get(url, verify=False)
    return request.text.encode('utf-8')


def parse(html):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      html.decode('utf-8'))
    return urls


@home.before_request
def make_session_permanent():
    session.permanent = True
    home.permanent_session_lifetime = timedelta(minutes=20)


@home.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Render the homepage template on the / route
    """
    form = CrawlUrlForm()
    if form.validate_on_submit():
        link = form.url.data
        session_id = session['csrf_token']

        # breaking down the url
        print(link, session)

        get_urls.apply_async(args=[session_id, link])
        return render_template('home/dashboard.html', title="Dashboard")
    return render_template('home/index.html', form=form, title="Welcome")


@celery.task
def get_urls(session_id, url):
    try:
        # for source_coordinates
        if not_in_db(url):
            save_url_to_db(session_id, url)
            html = crawl_url(url)
            urls = parse(html)
            for url in urls:
                get_urls.apply_async(args=[session_id, url])
            print(urls)

    except Exception as exception:
        print(exception)
