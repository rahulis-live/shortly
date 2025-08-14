from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import string
import re
from urllib.parse import urlparse
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ShortenedURL(db.Model):
    """Database model for storing URL mappings"""
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ShortenedURL {self.short_code}>'

def is_valid_url(url):
    """Validate if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def generate_short_code(length=6):
    """Generate a random short code for the URL"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route('/')
def index():
    """Main page with the URL shortening form"""
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to create a shortened URL"""
    data = request.get_json()
    original_url = data.get('url', '').strip()
    
    # Validate URL
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Add scheme if missing
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    # Check if URL already exists
    existing_url = ShortenedURL.query.filter_by(original_url=original_url).first()
    if existing_url:
        short_url = request.host_url.rstrip('/') + '/' + existing_url.short_code
        return jsonify({
            'original_url': original_url,
            'short_url': short_url,
            'short_code': existing_url.short_code,
            'message': 'URL already shortened'
        })
    
    # Generate unique short code
    while True:
        short_code = generate_short_code()
        if not ShortenedURL.query.filter_by(short_code=short_code).first():
            break
    
    # Create new shortened URL
    shortened_url = ShortenedURL(original_url=original_url, short_code=short_code)
    db.session.add(shortened_url)
    db.session.commit()
    
    short_url = request.host_url.rstrip('/') + '/' + short_code
    
    return jsonify({
        'original_url': original_url,
        'short_url': short_url,
        'short_code': short_code,
        'message': 'URL shortened successfully'
    })

@app.route('/<short_code>')
def redirect_to_original(short_code):
    """Redirect short code to original URL"""
    shortened_url = ShortenedURL.query.filter_by(short_code=short_code).first()
    
    if not shortened_url:
        return render_template('404.html'), 404
    
    # Increment click counter
    shortened_url.clicks += 1
    db.session.commit()
    
    return redirect(shortened_url.original_url)

@app.route('/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a shortened URL"""
    shortened_url = ShortenedURL.query.filter_by(short_code=short_code).first()
    
    if not shortened_url:
        return jsonify({'error': 'URL not found'}), 404
    
    return jsonify({
        'original_url': shortened_url.original_url,
        'short_code': shortened_url.short_code,
        'clicks': shortened_url.clicks,
        'created_at': shortened_url.created_at.isoformat()
    })

@app.route('/features')
def features():
    """Features page"""
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/resources')
def resources():
    """Resources page"""
    return render_template('resources.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
