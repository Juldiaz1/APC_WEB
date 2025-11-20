**# APC Database Web Interface

A Flask web application for managing the Arlington Physicians' Center database.

## Quick Start

### Clone and Setup
```bash
# Clone the repository
git clone https://github.com/Juldiaz1/APC_WEB.git
cd APC_WEB

# Install dependencies
pip install -r requirements.txt

# Configure database (edit config.py with your credentials)
# Run the application
python app.py
```

### Access the Application
Open your browser and go to: `http://127.0.0.1:5000`

## Configuration

Edit `config.py` with your MySQL settings:
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'apc_database', 
    'user': 'root',
    'password': 'your_password',
    'port': 3306
}
```

## Features

- Hospital and physician management
- Patient records and insurance details
- Consultation scheduling
- Database analytics and views

## Requirements

- Python 3.7+
- MySQL with APC database
- Flask, mysql-connector-python**
