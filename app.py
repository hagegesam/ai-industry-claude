from flask import Flask, render_template, jsonify
from database import DatabaseManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
db_manager = DatabaseManager()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/use-cases')
def get_use_cases():
    """Get all AI use cases from the database."""
    try:
        # Get all industries from the database
        industries = db_manager.get_all_industries()
        
        # Get use cases for each industry
        use_cases = {}
        for industry in industries:
            use_cases[industry] = db_manager.get_use_cases_by_industry(industry)
        
        return jsonify({
            'success': True,
            'data': use_cases
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 