# passenger_wsgi.py
import os
import sys
from hbhr import create_app

sys.path.append(os.path.dirname(__file__))

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)

application = app
