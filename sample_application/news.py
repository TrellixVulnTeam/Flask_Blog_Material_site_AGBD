from flask import Blueprint, render_template, redirect, url_for,request,jsonify
from .utils import get_words,revword
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
news = Blueprint('news', __name__)
from .model import *
from flask_login import current_user
from .utils import get_dict


@news.route('/news')
@news.route('/news/<int:page>')
def review_list(page=1):
    # image = 'images/coffee.jpg'
    # search_code = Code.objects( Q(published =True) & Q(category = 'google_customs_search_js')).first() or "something wrong"
    post = Info.objects(done=True).paginate(page=page, per_page=8)
    return render_template("news_nav.html", post=post, user=current_user)


@news.route('/news/<string:post_title>')
def get_post(post_title):
    post = Info.objects.get_or_404(title__contains=post_title)
    word = words.objects(title__contains=post_title).to_json()
    return render_template("trans.html", post=post, user=current_user,word = word)

@news.route('/news/words',methods=['GET', 'POST'])
def save_word():
    if request.method == "POST":
        data = urlparse.unquote(request.json['data'])
        loc = request.json['location']
        title = request.json['title']
        i_data = get_words(data)
        for x in i_data:
            dic = get_dict(revword(x[0]))
            if dic:
                words(word = revword(x[0]),exp = revword(x[1]),des = revword(x[2]),url = loc,title = title,dic =dic ).save()
    return str(len(i_data))


@news.route('/news_tag/<string:id>')
def view_tag_tags(id, page=1):
    # image = 'images/coffee.jpg'
    tags_post = Tag.objects(cata='Post')
    tags_reviews = Tag.objects(cata='Reviews')
    tags_news = Tag.objects(cata='News')
    post = Info.objects(done=True).filter(tags__in=[id])
    i = Image.objects(to_pub=True)[:3]
    tag = Tag.objects(id=id).first()
    # paginated_tags = post.paginate_field('tags', page=1, per_page=5)
    return render_template("news_tag.html", paginated_tags=post, image=i, tags_post=tags_post, tags_news=tags_news,
                           tags_reviews=tags_reviews, tag=tag, user=current_user)
