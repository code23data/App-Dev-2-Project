# Instructions for running the application
You will need a bash terminal to run the following commands as given below. You will also need to have redis server and MailHog installed.
1. Navigate to the root folder.
2. Open two separate terminals and run the following commands:
   - ``` redis-server --port 6380```
   - ```~/go/bin/MailHog```
3. Navigate to backend folder, and create a virtual environment by running the following commands in sequence:
   - ```python3 -m venv .venv```
   - ```source .venv/bin/activate```
   - ```pip install -r requirements.txt```
4. Now, staying in the backend folder, run the following commands in three separate terminals:
   - ```python main.py```
   - ```celery -A main.celery worker -l info```
   - ```celery -A main.celery beat --max-interval 1 -l info```
5. Now navigate to the frontend folder, and run the following command in the terminal:
   - ```npm install```
6. After installation in the frontend folder, run the following command in the frontend folder:
   - ```npm run serve```
These steps once executed successfully will have the application running successfully. You can view the application in your local browser at [http://localhost:5000](http://localhost:5000).
