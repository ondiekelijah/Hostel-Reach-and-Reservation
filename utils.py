import secrets
import os
import bs4
import urllib, re
from PIL import Image
# from . import app
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    send_from_directory,
)
from flask import current_app


def extract_text(url):
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    texts = soup.findAll(text=True)
    return texts

def is_visible(element):
    if element.parent.name in ["style", "script", "[document]", "head", "title"]:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == "\n":
        return False
    return True


def filter_visible_text(page_texts):
    return filter(is_visible, page_texts)


WPM = 200
WORD_LENGTH = 5


def count_words_in_text(text_list, word_length):
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text) / word_length
    return total_words


def estimate_reading_time(url):
    texts = extract_text(url)
    filtered_text = filter_visible_text(texts)
    total_words = count_words_in_text(filtered_text, WORD_LENGTH)
    read_time = int(total_words / WPM)
    return read_time

def upload_img(post_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(post_img.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/images/blog-posts", picture_filename
    )
    post_img.save(picture_path)
    return picture_filename

def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/images/ProfileImages", picture_fn
    )
    form_img.save(picture_path)

    return picture_fn

def redirect_url(default='index'):
    return request.args.get('next') or \
           back_url or \
           url_for(default)
           