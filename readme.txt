-> Install Flask using the following command in the command prompt:

"pip install flask"


-> Open a command prompt and navigate to the directory containing rec.py.

-> Run the following command in the command prompt:

"set FLASK_APP=rec.py"

This command sets the environment variable FLASK_APP to rec.py.

-> Run the following command to start the Flask server:

"flask run"

This command will start the Flask server on http://127.0.0.1:5000/.

-> To test the API, open a web browser and go to http://127.0.0.1:5000/. You should see the output of your Flask API in JSON format.
Alternatively, you can use a tool like curl or Postman to send HTTP requests to your API and get the results. For example, to get the top 5 recommended cuisines for user with ID 1098, you can send a GET request to http://127.0.0.1:5000/recommend/1098/5.