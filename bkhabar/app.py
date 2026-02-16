"""
BKhabar - Bangladeshi Food Delivery App
A complete food delivery system with bKash, Nagad, and Card payment support
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import sqlite3
import json
import os
import uuid
import hashlib
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'bkhabar-secret-key-change-this-in-production'

# ─────────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────────

def get_db():
    db = sqlite3.connect('bkhabar.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS orders (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            phone       TEXT NOT NULL,
            address     TEXT NOT NULL,
            area        TEXT NOT NULL,
            items       TEXT NOT NULL,
            subtotal    REAL NOT NULL,
            delivery    REAL NOT NULL,
            total       REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT DEFAULT 'pending',
            order_status   TEXT DEFAULT 'placed',
            created_at     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS menu_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            name_bn     TEXT NOT NULL,
            category    TEXT NOT NULL,
            price       REAL NOT NULL,
            description TEXT,
            emoji       TEXT,
            popular     INTEGER DEFAULT 0
        );
    ''')
    db.commit()

    # Seed menu if empty
    count = db.execute('SELECT COUNT(*) FROM menu_items').fetchone()[0]
    if count == 0:
        menu = [
            # Biryani & Rice
            ('Kacchi Biryani', 'কাচ্চি বিরিয়ানি', 'Biryani & Rice', 320, 'Authentic Dhaka-style mutton kacchi with potato & egg', '🍖', 1),
            ('Chicken Biryani', 'চিকেন বিরিয়ানি', 'Biryani & Rice', 250, 'Aromatic basmati rice with tender spiced chicken', '🍗', 1),
            ('Tehari', 'তেহারি', 'Biryani & Rice', 220, 'Traditional Dhaka beef tehari with fragrant spices', '🍛', 1),
            ('Beef Kala Bhuna', 'গরুর কালা ভুনা', 'Biryani & Rice', 280, 'Slow-cooked Chittagong-style beef black curry', '🥩', 0),
            ('Plain Rice', 'সাদা ভাত', 'Biryani & Rice', 40, 'Steamed white rice', '🍚', 0),

            # Fish Dishes
            ('Ilish Bhapa', 'ইলিশ ভাপা', 'Fish & Seafood', 350, 'Steamed hilsa with mustard & coconut paste', '🐟', 1),
            ('Rui Macher Jhol', 'রুই মাছের ঝোল', 'Fish & Seafood', 200, 'Light spiced rohu fish curry', '🐠', 0),
            ('Chingri Malaikari', 'চিংড়ি মালাইকারি', 'Fish & Seafood', 380, 'Prawns in creamy coconut milk sauce', '🦐', 1),
            ('Shutki Bhuna', 'শুঁটকি ভুনা', 'Fish & Seafood', 180, 'Spicy dried fish stir-fry, a Bangladeshi classic', '🐡', 0),

            # Meat Dishes
            ('Beef Rezala', 'গরুর রেজালা', 'Meat Dishes', 290, 'Mughal-style white gravy beef with sour yogurt', '🥘', 1),
            ('Chicken Bhuna', 'চিকেন ভুনা', 'Meat Dishes', 240, 'Dry-roasted chicken with whole spices', '🍗', 0),
            ('Mutton Curry', 'মটন কারি', 'Meat Dishes', 310, 'Slow-cooked goat meat in rich gravy', '🐑', 0),
            ('Beef Nihari', 'গরুর নিহারি', 'Meat Dishes', 300, 'Morning stew of beef shank, best with naan', '🍲', 1),

            # Street Food
            ('Fuchka (6 pcs)', 'ফুচকা', 'Street Food', 60, 'Crispy hollow puri with tamarind & spiced filling', '🫙', 1),
            ('Chotpoti', 'চটপটি', 'Street Food', 80, 'Spiced chickpea & potato with egg & chutney', '🥗', 1),
            ('Halim', 'হালিম', 'Street Food', 150, 'Slow-cooked lentil & meat stew, Dhaka special', '🍜', 1),
            ('Jhal Muri', 'ঝাল মুড়ি', 'Street Food', 50, 'Spicy puffed rice with mustard oil & veggies', '🌶️', 0),
            ('Samosa (4 pcs)', 'সামোসা', 'Street Food', 80, 'Crispy fried pastry with spiced potato filling', '🥟', 0),

            # Dal & Vegetarian
            ('Dal Makhani', 'ডাল মাখানি', 'Dal & Vegetarian', 120, 'Creamy black lentil curry cooked overnight', '🫘', 0),
            ('Begun Bhaja', 'বেগুন ভাজা', 'Dal & Vegetarian', 80, 'Crispy fried eggplant slices', '🍆', 0),
            ('Shukto', 'শুক্তো', 'Dal & Vegetarian', 100, 'Bitter melon mixed vegetable curry', '🥬', 0),
            ('Cholar Dal', 'ছোলার ডাল', 'Dal & Vegetarian', 110, 'Festive chickpea dal with coconut', '🟡', 1),

            # Breads
            ('Naan (2 pcs)', 'নান', 'Breads', 60, 'Soft leavened flatbread from tandoor', '🫓', 0),
            ('Paratha (2 pcs)', 'পরাটা', 'Breads', 50, 'Flaky layered whole wheat flatbread', '🫓', 1),
            ('Luchi (4 pcs)', 'লুচি', 'Breads', 60, 'Deep-fried fluffy white flour puri', '⭕', 0),

            # Desserts & Drinks
            ('Mishti Doi', 'মিষ্টি দই', 'Desserts & Drinks', 80, 'Sweet fermented yogurt, a Bengali specialty', '🍮', 1),
            ('Rosogolla (4 pcs)', 'রসগোল্লা', 'Desserts & Drinks', 100, 'Spongy cottage cheese balls in sugar syrup', '🍡', 1),
            ('Borhani', 'বোরহানি', 'Desserts & Drinks', 60, 'Savory spiced yogurt drink with mint & cumin', '🥛', 1),
            ('Faluda', 'ফালুদা', 'Desserts & Drinks', 120, 'Rose milk with basil seeds, vermicelli & ice cream', '🧁', 0),
            ('Lassi', 'লাচ্ছি', 'Desserts & Drinks', 80, 'Thick yogurt drink, sweet or salted', '🥤', 0),
        ]
        db.executemany(
            'INSERT INTO menu_items (name, name_bn, category, price, description, emoji, popular) VALUES (?,?,?,?,?,?,?)',
            menu
        )
        db.commit()
    db.close()


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    db = get_db()
    items = db.execute('SELECT * FROM menu_items ORDER BY popular DESC, category, name').fetchall()
    db.close()

    # Organize by category
    menu = {}
    for item in items:
        cat = item['category']
        if cat not in menu:
            menu[cat] = []
        menu[cat].append(dict(item))

    cart = session.get('cart', {})
    cart_count = sum(v['qty'] for v in cart.values())
    return render_template('index.html', menu=menu, cart_count=cart_count)


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_count = sum(v['qty'] for v in cart.values())
    total = sum(v['price'] * v['qty'] for v in cart.values())
    return render_template('cart.html', cart=cart, total=total, cart_count=cart_count)


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_id = str(data['id'])
    db = get_db()
    item = db.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,)).fetchone()
    db.close()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    cart = session.get('cart', {})
    if item_id in cart:
        cart[item_id]['qty'] += 1
    else:
        cart[item_id] = {
            'id': item_id,
            'name': item['name'],
            'name_bn': item['name_bn'],
            'price': item['price'],
            'emoji': item['emoji'],
            'qty': 1
        }
    session['cart'] = cart
    total_items = sum(v['qty'] for v in cart.values())
    return jsonify({'success': True, 'cart_count': total_items})


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    item_id = str(data['id'])
    qty = int(data['qty'])
    cart = session.get('cart', {})
    if qty <= 0:
        cart.pop(item_id, None)
    elif item_id in cart:
        cart[item_id]['qty'] = qty
    session['cart'] = cart
    total = sum(v['price'] * v['qty'] for v in cart.values())
    cart_count = sum(v['qty'] for v in cart.values())
    return jsonify({'success': True, 'total': total, 'cart_count': cart_count})


@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return jsonify({'success': True})


@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
    subtotal = sum(v['price'] * v['qty'] for v in cart.values())
    cart_count = sum(v['qty'] for v in cart.values())

    areas = [
        'Dhanmondi', 'Gulshan', 'Banani', 'Mirpur', 'Uttara',
        'Mohammadpur', 'Motijheel', 'Old Dhaka', 'Bashundhara',
        'Wari', 'Rampura', 'Badda', 'Khilgaon', 'Jatrabari',
        'Demra', 'Shyamoli', 'Tejgaon'
    ]
    return render_template('checkout.html', cart=cart, subtotal=subtotal,
                           areas=areas, cart_count=cart_count)


@app.route('/place-order', methods=['POST'])
def place_order():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))

    name    = request.form.get('name', '').strip()
    phone   = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    area    = request.form.get('area', '').strip()
    payment = request.form.get('payment', 'cod')

    if not all([name, phone, address, area]):
        flash('সব তথ্য পূরণ করুন। Please fill all fields.', 'error')
        return redirect(url_for('checkout'))

    subtotal = sum(v['price'] * v['qty'] for v in cart.values())
    delivery = 0 if subtotal >= 500 else 60
    total    = subtotal + delivery

    order_id = str(uuid.uuid4())[:8].upper()

    db = get_db()
    db.execute('''
        INSERT INTO orders (id, name, phone, address, area, items, subtotal, delivery, total,
                           payment_method, payment_status, order_status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_id, name, phone, address, area,
        json.dumps(list(cart.values())),
        subtotal, delivery, total,
        payment,
        'pending' if payment == 'cod' else 'awaiting',
        'placed',
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    db.commit()
    db.close()

    # For mobile banking payments redirect to payment page
    if payment in ('bkash', 'nagad', 'rocket'):
        session['pending_order'] = order_id
        session['cart'] = {}
        return redirect(url_for('payment_gateway', method=payment, order_id=order_id))

    # For card payment
    if payment == 'card':
        session['pending_order'] = order_id
        session['cart'] = {}
        return redirect(url_for('payment_gateway', method='card', order_id=order_id))

    # Cash on Delivery
    session['cart'] = {}
    session.pop('pending_order', None)
    return redirect(url_for('order_success', order_id=order_id))


@app.route('/payment/<method>/<order_id>')
def payment_gateway(method, order_id):
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    db.close()
    if not order:
        return redirect(url_for('index'))
    return render_template('payment.html', method=method, order=dict(order))


@app.route('/confirm-payment/<order_id>', methods=['POST'])
def confirm_payment(order_id):
    """Simulate payment confirmation (in production use real gateway callbacks)"""
    txn_id = request.form.get('txn_id', '').strip()
    method = request.form.get('method', '')

    if not txn_id or len(txn_id) < 6:
        flash('অবৈধ ট্রানজেকশন আইডি। Invalid transaction ID.', 'error')
        return redirect(url_for('payment_gateway', method=method, order_id=order_id))

    db = get_db()
    db.execute(
        'UPDATE orders SET payment_status = ?, order_status = ? WHERE id = ?',
        ('paid', 'confirmed', order_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('order_success', order_id=order_id))


@app.route('/order/<order_id>')
def order_success(order_id):
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    db.close()
    if not order:
        return redirect(url_for('index'))
    order = dict(order)
    order['items'] = json.loads(order['items'])
    cart_count = 0
    return render_template('success.html', order=order, cart_count=cart_count)


@app.route('/track/<order_id>')
def track_order(order_id):
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    db.close()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    order = dict(order)
    order['items'] = json.loads(order['items'])
    return jsonify(order)


# ─────────────────────────────────────────────
#  ADMIN (simple, password-protected)
# ─────────────────────────────────────────────

ADMIN_PASSWORD = 'admin123'  # Change this!

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
        else:
            flash('Wrong password!', 'error')

    if not session.get('admin'):
        return render_template('admin_login.html')

    db = get_db()
    orders = db.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    db.close()
    orders = [dict(o) for o in orders]
    for o in orders:
        o['items'] = json.loads(o['items'])
    return render_template('admin.html', orders=orders)


@app.route('/admin/update-status', methods=['POST'])
def update_order_status():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    db = get_db()
    db.execute('UPDATE orders SET order_status = ? WHERE id = ?',
               (data['status'], data['order_id']))
    db.commit()
    db.close()
    return jsonify({'success': True})


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    print("\n🍛 BKhabar Food Delivery is running!")
    print("🌐 Open: http://localhost:5000")
    print("🔐 Admin: http://localhost:5000/admin  (password: admin123)\n")
    app.run(debug=True, port=5000)

dir