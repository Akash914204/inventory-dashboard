#!/bin/bash
# Example run script for production demo (simple)
cd "$(dirname "$0")"
export FLASK_APP=app.py
export FLASK_ENV=production
python3 app.py >> /var/log/inventory_app.log 2>&1 &
echo $! > /var/run/inventory_app.pid

#!/bin/bash
echo "Starting Flask Inventory Management Dashboard..."
source venv/bin/activate
flask run --host=0.0.0.0 --port=5000
