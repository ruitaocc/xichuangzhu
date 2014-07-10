# coding: utf-8
from flask import render_template, request, redirect, url_for, Blueprint
from ..models import db, Author, Quote, Work, WorkType, CollectWork, Dynasty
from ..permissions import admin_permission
from ..forms import AuthorForm, AuthorQuoteForm

bp = Blueprint('author', __name__)


@bp.route('/<author_abbr>')
def view(author_abbr):
    """文学家主页"""
    author = Author.query.filter(Author.abbr == author_abbr).first_or_404()
    quote_id = request.args.get('q')
    quote = Quote.query.get(quote_id) if quote_id else None
    if not quote:
        quote = author.random_quote
    stmt = db.session.query(Work.type_id, db.func.count(Work.type_id).label('type_num')).filter(
        Work.author_id == author.id).group_by(Work.type_id).subquery()
    work_types = db.session.query(WorkType, stmt.c.type_num) \
        .join(stmt, WorkType.id == stmt.c.type_id)
    return render_template('author/author.html', author=author, quote=quote, work_types=work_types)


@bp.route('/')
def authors():
    """全部文学家"""
    # 仅获取包含至少1个文学家的朝代
    dynasties = Dynasty.query.filter(Dynasty.authors.any()).order_by(Dynasty.start_year.asc())
    # get the authors who's works are latest collected by user
    stmt = db.session.query(Author.id, CollectWork.create_time).join(Work).join(
        CollectWork).group_by(Author.id).having(
        db.func.max(CollectWork.create_time)).subquery()
    hot_authors = Author.query.join(stmt, Author.id == stmt.c.id).order_by(
        stmt.c.create_time.desc()).limit(8)
    return render_template('author/authors.html', dynasties=dynasties, hot_authors=hot_authors)


@bp.route('/add', methods=['GET', 'POST'])
@admin_permission
def add():
    """添加文学家"""
    form = AuthorForm()
    form.dynasty_id.choices = [(d.id, d.name) for d in Dynasty.query.order_by(Dynasty.start_year)]
    if form.validate_on_submit():
        author = Author(**form.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('.view', author_abbr=author.abbr))
    return render_template('author/add.html', form=form)


@bp.route('/<int:author_id>/edit', methods=['GET', 'POST'])
@admin_permission
def edit(author_id):
    """编辑文学家"""
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)
    form.dynasty_id.choices = [(d.id, d.name) for d in Dynasty.query.order_by(Dynasty.start_year)]
    if form.validate_on_submit():
        form.populate_obj(author)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('.view', author_abbr=author.abbr))
    return render_template('author/edit.html', author=author, form=form)


@bp.route('/<int:author_id>/add_quote', methods=['GET', 'POST'])
@admin_permission
def add_quote(author_id):
    """管理文学家的名言"""
    author = Author.query.get_or_404(author_id)
    form = AuthorQuoteForm()
    if form.validate_on_submit():
        quote = Quote(quote=form.quote.data, work_id=form.work_id.data, author_id=author_id)
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('.view', author_abbr=author.abbr))
    return render_template('author/add_quote.html', author=author, form=form)


@bp.route('/quote/<int:quote_id>/edit', methods=['GET', 'POST'])
@admin_permission
def edit_quote(quote_id):
    """编辑名言"""
    quote = Quote.query.get_or_404(quote_id)
    form = AuthorQuoteForm(obj=quote)
    if form.validate_on_submit():
        form.populate_obj(quote)
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('.view', author_abbr=quote.author.abbr))
    return render_template('author/edit_quote.html', quote=quote, form=form)


@bp.route('/quote/<int:quote_id>/delete')
@admin_permission
def delete_quote(quote_id):
    """删除名言"""
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('.view', author_abbr=quote.author.abbr))
