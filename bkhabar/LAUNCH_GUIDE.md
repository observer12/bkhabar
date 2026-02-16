# 🍛 BKhabar — Complete Launch Guide
### বাংলার স্বাদ ঘরে পৌঁছে দেই | From Zero to Live in Bangladesh

---

## 📋 WHAT YOU GET
- Full food delivery website in Python (Flask)
- 30+ Bangladeshi menu items (Kacchi, Ilish, Fuchka, etc.)
- bKash, Nagad, Rocket, Card & Cash on Delivery
- Beautiful Bengali-themed UI
- Admin dashboard to manage orders
- Order tracking system

---

## 🖥️ STEP 1 — RUN ON YOUR COMPUTER (Local Testing)

### A) Install Python
1. Go to https://python.org/downloads
2. Download Python 3.12 → Install it
3. During install ✅ CHECK "Add Python to PATH"

### B) Install the App
Open **Command Prompt** (press Win+R → type `cmd` → Enter):

```bash
# Go to your Downloads folder (or wherever you saved the app)
cd C:\Users\YourName\Downloads\bkhabar

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### C) Open in Browser
- Go to: **http://localhost:5000**
- Admin panel: **http://localhost:5000/admin** (password: admin123)

✅ Your app is running! Now let's put it on the internet.

---

## 🌐 STEP 2 — PUT IT ON THE INTERNET (Free Option: Render.com)

This is the **easiest free option** — no credit card needed for small traffic.

### A) Create GitHub Account
1. Go to https://github.com → Sign Up (free)
2. Click "New Repository" → Name it `bkhabar`
3. Make it Public → Create

### B) Upload Your Code to GitHub
```bash
# In your bkhabar folder, run:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/bkhabar.git
git push -u origin main
```

### C) Deploy on Render (FREE)
1. Go to https://render.com → Sign Up (free, use GitHub login)
2. Click **"New +" → "Web Service"**
3. Connect your GitHub → Select `bkhabar` repo
4. Fill in settings:
   - **Name:** bkhabar
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **"Create Web Service"**
6. Wait 3-5 minutes → You get a FREE link like: `https://bkhabar.onrender.com`

> ⚠️ Add `gunicorn==21.2.0` to requirements.txt before deploying

### Your app is now LIVE! Share the link with customers.

---

## 💰 STEP 3 — REAL PAYMENT GATEWAY SETUP

### Option A: bKash Payment Gateway (Official)
1. Register your business: https://developer.bkash.com
2. Get **AppKey, AppSecret, Username, Password**
3. Replace the payment simulation in `app.py` with bKash Checkout API
4. Cost: Free integration, bKash charges ~1.5% transaction fee

### Option B: Nagad Payment Gateway
1. Register: https://nagad.com.bd/merchant
2. Contact: merchant@nagad.com.bd
3. They'll give you API credentials

### Option C: SSLCommerz (All-in-one — Cards + bKash + Nagad)
This is the BEST option for Bangladesh. It supports EVERYTHING.
1. Register: https://sslcommerz.com/product/sslereg
2. Get Store ID and Store Password (sandbox first)
3. Integration docs: https://developer.sslcommerz.com
4. Install: `pip install sslcommerz-lib`
5. Charges: 1.5% - 2.5% per transaction
6. Supports: Visa, Mastercard, bKash, Nagad, Rocket, Dutch-Bangla

### Option D: ShurjoPay (Bangladeshi alternative)
1. Register: https://shurjopay.com.bd
2. Supports bKash, Nagad, Rocket, Cards
3. Easy integration with Python library

---

## 📱 STEP 4 — CUSTOM DOMAIN (Professional Look)

### Buy a .com.bd Domain (৳800-1200/year)
- **ExonHost:** https://exonhost.com (Bangladeshi company)
- **BD Web Host:** https://bdwebhost.com
- **Namecheap:** https://namecheap.com (international)

### Connect Domain to Render
1. In Render → Settings → Custom Domain
2. Enter your domain (e.g., `bkhabar.com.bd`)
3. Update DNS at your domain registrar

---

## 📊 STEP 5 — PRODUCTION SERVER (When You Scale Up)

For serious business with 100+ orders/day, use a VPS:

### DigitalOcean (Recommended for Bangladesh)
- Cost: $6/month
- Sign up: https://digitalocean.com
- Choose "Ubuntu 22.04" server in Singapore (closest to Bangladesh)

```bash
# On your server:
sudo apt update
sudo apt install python3-pip nginx

# Upload your code (use FileZilla or GitHub)
cd /var/www/bkhabar
pip3 install -r requirements.txt
pip3 install gunicorn

# Run with gunicorn (handles multiple users)
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Use nginx as reverse proxy (ask a developer to set this up)
```

### Bangladeshi Hosting Options
- **ExonHost VPS:** https://exonhost.com (BDT 1500/month, good support)
- **Host Mighty:** https://hostmighty.com
- **Zaman IT:** https://zamanit.com

---

## 📲 STEP 6 — MAKE IT A MOBILE APP (Optional)

### Convert Website to App — FREE Method
Use **WebViewGold** or **Median.co**:
1. Go to https://median.co → Paste your website URL
2. They build an Android & iOS app for you
3. Publish to Google Play Store (~$25 one-time fee)

### Flutter App (Need Developer)
Hire a developer on:
- **Fiverr.com** — $50-200 for a simple delivery app
- **Upwork.com** — Bangladeshi developers available
- **Facebook Groups** — "Bangladesh Freelancer Community"

---

## 🔧 STEP 7 — IMPORTANT CHANGES BEFORE GOING LIVE

Open `app.py` and change these:

```python
# Line 1: Change secret key (make it random!)
app.secret_key = 'make-this-very-long-and-random-abc123xyz789'

# Admin password (change from admin123!)
ADMIN_PASSWORD = 'YourStrongPassword@2024'

# Your phone number for payment
# In payment.html, replace 01700-000000 with your bKash number
```

---

## 📦 STEP 8 — BUSINESS REQUIREMENTS IN BANGLADESH

To operate legally:
1. **Trade License** from your local City Corporation (৳1000-5000)
2. **TIN Certificate** from National Board of Revenue (free)
3. **bKash Merchant Account** — needs Trade License
4. **Food Safety License** from BFSA if you're making food

---

## 🚀 QUICK REFERENCE CHECKLIST

- [ ] Run locally: `python app.py`
- [ ] Change admin password in `app.py`
- [ ] Change secret key in `app.py`
- [ ] Add your bKash/Nagad number in `payment.html`
- [ ] Update menu prices and items as needed
- [ ] Deploy to Render.com (free)
- [ ] Set up SSLCommerz for real payments
- [ ] Buy a domain (optional)
- [ ] Get Trade License for merchant payment

---

## 📞 NEED HELP?

If you get stuck at any step:
1. Search the error on Google with "Flask Python" or "Render.com"
2. Ask on Stack Overflow: https://stackoverflow.com
3. Bangladesh developer Facebook groups
4. Hire help on Fiverr for ~$10-20

---

*BKhabar v1.0 — Built for Bangladesh 🇧🇩*
