## Prerequisites

- Python 3.8 or higher
- Azure account with Computer Vision API access
- Git

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/realAkshaj/moments-cs516.git
cd moments-cs516
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On Linux/Mac:
source env/bin/activate
# On Windows:
# env\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues with dependencies, install them manually:

```bash
pip install flask flask-sqlalchemy flask-migrate flask-wtf flask-login
pip install flask-mail flask-moment python-dotenv pillow email-validator
pip install flask-avatars whoosh
pip install azure-cognitiveservices-vision-computervision msrest
```

### 4. Set Up Azure Computer Vision API

#### Create Azure Resource:
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new "Computer Vision" resource
3. Choose the **Free F0** pricing tier (5,000 API calls/month)
4. Select a region close to you

#### Get API Credentials:
1. Go to your Computer Vision resource
2. Click "Keys and Endpoint" in the left sidebar
3. Copy **Key 1** and **Endpoint URL**

#### Configure API Keys:
```bash
# Create config directory
mkdir -p config

# Create API keys file
cat > config/api_keys.py << 'EOF'
# Azure Computer Vision API credentials
AZURE_VISION_KEY = "your-api-key-here"
AZURE_VISION_ENDPOINT = "https://your-endpoint.cognitiveservices.azure.com/"
EOF
```

**Replace the placeholder values with your actual Azure credentials.**

### 5. Initialize Database

```bash
# Set Flask app
export FLASK_APP="moments:create_app('development')"

# Initialize database
flask init-app

# Generate sample data (optional)
flask lorem
```

### 6. Run the Application

```bash
flask run
```

The application will be available at: http://127.0.0.1:5000/

### 7. Login

Use the test account:
- **Email**: `admin@helloflask.com`
- **Password**: `moments`

## Testing the ML Features

### Alt Text Generation
1. Upload a new image through the web interface
2. View the uploaded photo
3. Right-click on the image → "Inspect Element"
4. Look for the `alt` attribute containing the generated description

### Image Search
1. Upload images with recognizable objects (buildings, people, animals, etc.)
2. Use the search function to search for objects like "building", "person", "outdoor"
3. Images with matching ML-detected tags will appear in results

## Project Structure

```
moments-cs516/
├── config/
│   ├── __init__.py
│   └── api_keys.py          # Azure API credentials (not in git)
├── utils/
│   ├── __init__.py
│   └── azure_vision.py      # Azure Computer Vision service
├── moments/                 # Main Flask application
│   ├── blueprints/
│   │   └── main.py         # Routes with ML integration (lines 89-120)
│   ├── models.py           # Database models with alt_text and ml_tags fields
│   ├── templates/main/     # HTML templates with accessibility features
│   └── ...
├── requirements.txt        # Python dependencies
├── data-dev.db            # SQLite database
└── README.md
```

## Implementation Details

### Alt Text Generation
- Implemented in `moments/blueprints/main.py` upload route (lines 100-115)
- Uses Azure Computer Vision describe_image_in_stream API
- Stores generated text in `alt_text` database field
- Displays in HTML `alt` attributes via template updates

### Image Search Enhancement
- Object detection in upload route using analyze_image_in_stream API
- Detected objects stored in `ml_tags` field as comma-separated values
- Search function enhanced to query both description and ml_tags fields
- Case-insensitive search implementation

### Database Schema
New fields added to Photo model:
- `alt_text VARCHAR(500)`: Stores ML-generated alternative text
- `ml_tags TEXT`: Stores detected objects as searchable tags

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Migrate
- **ML Service**: Azure Computer Vision API
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap, Jinja2 templates
- **Authentication**: Flask-Login
- **Image Processing**: Pillow (PIL)

## Troubleshooting

### Database Issues
```bash
# If database doesn't exist or has issues
rm data-dev.db
flask init-app
flask lorem
```

### Azure API Issues
- Verify your API key and endpoint in `config/api_keys.py`
- Check your Azure resource is active and has available quota
- Ensure you're using the correct region endpoint

### Dependencies
- If PIL/Pillow fails, install system dependencies: `sudo apt-get install python3-dev`
- For older Python versions, try: `pip install --upgrade setuptools wheel`

### Import Errors
```bash
# Test Azure Vision import
python -c "from utils.azure_vision import vision_service; print('Azure Vision loaded successfully')"
```

## Security Notes

- API credentials are stored in `config/api_keys.py` which is excluded from version control
- Never commit API keys to the repository
- Use environment variables for production deployments

## Assignment Context

This project was developed for CS516 (Machine Learning in Production) to demonstrate:
- Integration of ML services into web applications
- Accessibility improvements through automated alt text
- Enhanced search functionality via computer vision
- Production considerations for ML-enabled sys
