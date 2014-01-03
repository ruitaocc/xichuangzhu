# coding: utf-8
from flask import render_template, request, redirect, url_for
from xichuangzhu import app, db
from xichuangzhu.models.author import Author, AuthorQuote
from xichuangzhu.models.work import Work, WorkType
from xichuangzhu.models.collect import CollectWork
from xichuangzhu.models.dynasty import Dynasty
from xichuangzhu.utils import require_admin


@app.route('/author/<author_abbr>')
def author(author_abbr):
    """文学家主页"""
    author = Author.query.options(db.subqueryload(Author.works)).filter(Author.abbr == author_abbr).first_or_404()
    quote = AuthorQuote.query.get_or_404(int(float(request.args['q']))) if 'q' in request.args else author.random_quote
    stmt = db.session.query(Work.type_id, db.func.count(Work.type_id).label('type_num')).filter(
        Work.author_id == author.id).group_by(Work.type_id).subquery()
    work_types = db.session.query(WorkType, stmt.c.type_num).join(stmt, WorkType.id == stmt.c.type_id)
    return render_template('author/author.html', author=author, quote=quote, work_types=work_types)


@app.route('/authors')
def authors():
    """全部文学家"""
    dynasties = Dynasty.query.filter(Dynasty.authors.any()).order_by(Dynasty.start_year)
    # get the authors who's works are latest collected by user
    stmt = db.session.query(Author.id, CollectWork.create_time).join(Work).join(CollectWork).group_by(Author.id).having(
        db.func.max(CollectWork.create_time)).subquery()
    hot_authors = Author.query.join(stmt, Author.id == stmt.c.id).order_by(stmt.c.create_time.desc()).limit(8)
    return render_template('author/authors.html', dynasties=dynasties, hot_authors=hot_authors)


@app.route('/author/add', methods=['GET', 'POST'])
@require_admin
def add_author():
    """添加文学家"""
    if request.method == 'GET':
        dynasties = Dynasty.query.order_by(Dynasty.start_year)
        return render_template('author/add_author.html', dynasties=dynasties)
    else:
        author = Author(name=request.form['name'], abbr=request.form['abbr'], intro=request.form['intro'],
                        birth_year=request.form['birth_year'], death_year=request.form['death_year'],
                        dynasty_id=int(request.form['dynasty_id']))
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('author', author_abbr=author.abbr))

# page edit author
#--------------------------------------------------
@app.route('/author/<int:author_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_author(author_id):
    """编辑文学家"""
    author = Author.query.get_or_404(author_id)
    if request.method == 'GET':
        dynasties = Dynasty.query.order_by(Dynasty.start_year)
        return render_template('author/edit_author.html', dynasties=dynasties, author=author)
    else:
        author.name = request.form['name']
        author.abbr = request.form['abbr']
        author.intro = request.form['intro']
        author.birth_year = request.form['birth_year']
        author.death_year = request.form['death_year']
        author.dynasty_id = int(request.form['dynasty_id'])
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('author', author_abbr=author.abbr))


@app.route('/author/<int:author_id>/admin_quote')
@require_admin
def admin_quotes(author_id):
    """管理文学家的名言"""
    author = Author.query.options(db.subqueryload(Author.quotes)).get_or_404(author_id)
    return render_template('author/admin_quotes.html', author=author)


@app.route('/author/<int:author_id>/add_quote', methods=['POST'])
@require_admin
def add_quote(author_id):
    """添加名言"""
    quote = AuthorQuote(quote=request.form['quote'], author_id=author_id, work_id=int(request.form['work_id']))
    db.session.add(quote)
    db.session.commit()
    return redirect(url_for('admin_quotes', author_id=author_id))


@app.route('/quote/<int:quote_id>/delete')
@require_admin
def delete_quote(quote_id):
    """删除名言"""
    quote = AuthorQuote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('admin_quotes', author_id=quote.author_id))


@app.route('/quote/<int:quote_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_quote(quote_id):
    """编辑名言"""
    if request.method == 'GET':
        quote = AuthorQuote.query.get_or_404(quote_id)
        return render_template('author/edit_quote.html', quote=quote)
    else:
        quote = AuthorQuote.query.get_or_404(quote_id)
        quote.quote = request.form['quote']
        quote.work_id = int(request.form['work_id'])
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('admin_quotes', author_id=quote.work.author_id))