#-*- coding: UTF-8 -*-

import markdown2
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu.models.product_model import Product
from xichuangzhu.utils import check_admin

# page - shop
#--------------------------------------------------

# view (public)
@app.route('/things')
def products():
	products = Product.get_products(12)
	return render_template('product/products.html', products=products)

# page - single product
#--------------------------------------------------

# view (public)
@app.route('/thing/<int:product_id>')
def single_product(product_id):
	product = Product.get_product(product_id)
	if not product:
		abort(404)
	product['Introduction'] = markdown2.markdown(product['Introduction'])
	return render_template('product/single_product.html', product=product)

# page - add product
#--------------------------------------------------

# view (admin)
@app.route('/thing/add', methods=['GET', 'POST'])
def add_product():
	check_admin()

	if request.method == 'GET':
		return render_template('product/add_product.html')
	elif request.method == 'POST':
		product = request.form['product']
		url = request.form['url']
		image_url = request.form['image-url']
		introduction = request.form['introduction']
		
		new_product_id = Product.add_product(product, url, image_url, introduction)
		return redirect(url_for('single_product', product_id=new_product_id))

# page - edit product
#--------------------------------------------------

# view (admin)
@app.route('/thing/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
	check_admin()
	
	if request.method == 'GET':
		product = Product.get_product(product_id)
		return render_template('product/edit_product.html', product=product)
	elif request.method == 'POST':
		product = request.form['product']
		url = request.form['url']
		image_url = request.form['image-url']
		introduction = request.form['introduction']

		Product.edit_product(product_id, product, url, image_url, introduction)
		return redirect(url_for('single_product', product_id=product_id))