# URL Shortener

A modern, responsive URL shortening web application built with Flask and SQLite. Transform long URLs into short, shareable links with a clean and professional interface.

## Features

- **URL Shortening**: Convert long URLs into short, memorable links
- **Click Tracking**: Monitor how many times each shortened link is accessed
- **URL Validation**: Automatic validation of input URLs
- **Duplicate Prevention**: Same URLs get the same short code
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations
- **Copy to Clipboard**: One-click copying of shortened URLs
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **404 Page**: Custom error page for invalid short codes

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## Project Structure

```
url2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md             # Project documentation
├── templates/
│   ├── index.html        # Main page template
│   └── 404.html          # Error page template
└── static/
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── script.js     # Frontend JavaScript
```

## Quick Start

### Option 1: Local Development

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd url2
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t url-shortener .
   docker run -p 5000:5000 url-shortener
   ```

## API Endpoints

### POST `/shorten`
Shorten a URL

**Request Body:**
```json
{
    "url": "https://example.com/very/long/url"
}
```

**Response:**
```json
{
    "original_url": "https://example.com/very/long/url",
    "short_url": "http://localhost:5000/abc123",
    "short_code": "abc123",
    "message": "URL shortened successfully"
}
```

### GET `/<short_code>`
Redirect to original URL

### GET `/stats/<short_code>`
Get statistics for a shortened URL

**Response:**
```json
{
    "original_url": "https://example.com/very/long/url",
    "short_code": "abc123",
    "clicks": 42,
    "created_at": "2023-12-01T10:30:00"
}
```

## Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key (default: 'your-secret-key-change-in-production')
- `FLASK_ENV`: Flask environment (default: 'development')

### Database

The application uses SQLite by default. The database file (`url_shortener.db`) will be created automatically when you first run the application.

## Features in Detail

### URL Validation
- Validates URL format using Python's `urllib.parse`
- Automatically adds `https://` scheme if missing
- Rejects invalid URLs with clear error messages

### Short Code Generation
- Generates 6-character alphanumeric codes
- Ensures uniqueness by checking against existing codes
- Uses cryptographically secure random generation

### Click Tracking
- Automatically increments click counter on each redirect
- Provides statistics endpoint for analytics
- Tracks creation date and time

### User Interface
- **Responsive Design**: Adapts to all screen sizes
- **Modern Styling**: Gradient backgrounds, smooth animations
- **Interactive Elements**: Hover effects, loading states
- **Accessibility**: Keyboard shortcuts, focus management
- **Error Handling**: Clear error messages and validation feedback

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Database Operations
The database is automatically created when the application starts. To reset the database:
```bash
rm url_shortener.db
python app.py
```

## Deployment

### Production Considerations

1. **Security**
   - Change the `SECRET_KEY` environment variable
   - Use HTTPS in production
   - Consider rate limiting for the `/shorten` endpoint

2. **Database**
   - For production, consider using PostgreSQL or MySQL
   - Implement database migrations for schema changes
   - Set up regular backups

3. **Performance**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Implement caching for frequently accessed URLs
   - Consider CDN for static assets

### Deployment Platforms

#### Render
1. Connect your repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Add environment variables

#### Railway
1. Connect your repository to Railway
2. Railway will automatically detect the Python app
3. Add environment variables in the dashboard

#### Heroku
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy using Heroku CLI or GitHub integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:
1. Check the documentation above
2. Look for existing issues in the repository
3. Create a new issue with detailed information

---

**Built with ❤️ using Flask and modern web technologies**
