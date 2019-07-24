Instruction to run the project:
-------------------------------

1. Install dependencies from requirements.txt

    pip install -r requirements.txt

2. Open the terminal, open project directory and then execute following commands:
      
      export FLASK_CONFIG=development
      
      export FLASK_APP=run.py
      
      flask db init
      
      flask db migrate
      
      flask db upgrade
      
      flask run

3. Run celery celery worker -A celery_worker.celery

4. Then visit http://127.0.0.1:5000 in your browser
