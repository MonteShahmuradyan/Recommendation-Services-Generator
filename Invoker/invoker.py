from flask import Flask, request, jsonify, Response, redirect
import requests
import json
import threading
from functools import lru_cache
import time
import redis as red
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)                              # Create the application                  

redis = red.Redis(host='redis', port=6379, db=0)   # Connect to redis to run in docker

# Local cache to store request and responds
local_cache = {}
TTL = 10                # TTL in 10 seconds
cache_lock = threading.Lock()      # thread-safe ops for cache

# This function clears local cache time to time
def clear_cache():
    while True:
        time.sleep(TTL)
        with cache_lock:
            local_cache.clear()

# # Start the cache-clearing thread
threading.Thread(target=clear_cache, daemon=True).start()

# this function sets the cache flow for Redis and local cache
def cache_set(key, value):
    with cache_lock:
        redis.setex(key, TTL, json.dumps(value))
        if len(local_cache) >= 3:                  # max 3 entries
            oldest_key = next(iter(local_cache))
            del local_cache[oldest_key]
        local_cache[key] = value

# This function gets cache flow from Redis or local cache

def cache_get(key):
    with cache_lock:
        value = redis.get(key)     #check cache in Redis
        if value:
            try:
                return json.loads(value.decode('utf-8'))
            except json.JSONDecodeError:
                return value.decode('utf-8')
        return local_cache.get(key)            # check local cache



@app.route('/recommend', methods=['POST'])   # the endpoint for recommendation requests
def recommend():
    data = request.form  # Get form data from POST request
    viewer_id = data.get('viewerid')

# If viewer id  is not available, it returns error
    if not viewer_id:                         
        return "<h1>Error: Missing viewerid parameter</h1>", 400

    # chech the cached response
    cached_response = cache_get(viewer_id)

    if cached_response:
        return format_recommendations(cached_response)

   # if not in cache, get recommendations.

    result = runcascade(viewer_id)
    cache_set(viewer_id, result)       # new results move to cache
    return format_recommendations(result)


# this function change the output of recommendation format into HTML
def format_recommendations(response):
    recommendations_html = "<h1>Recommendations:</h1><ul>"
    if isinstance(response, dict) and 'results' in response:
        for item in response['results']:
            recommendations_html += f"<li>Model: {item.get('reason')}, Result: {item.get('result')}</li>"
    recommendations_html += "</ul>"
    recommendations_html += '<a href="/post_request.html">Try Again</a>'
    return recommendations_html

# Function to make the requests to Generator service

def runcascade(viewer_id):
    model_names = ["model1", "model2", "model3", "model4", "model5"]
    responses = []

     # Generator service calling function
    def call_generator(model_name):
        try:
            response = requests.post(
                "http://generator:5001/generate",
                json={"model_name": model_name, "viewerid": viewer_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed for the model {model_name}: {e}")
            responses.append({"error": str(e)})

                 # ThreadPoolExecutor is making simultaneous requests
    with ThreadPoolExecutor(max_workers=len(model_names)) as executor:
        features = [executor.submit(call_generator, model_name) for model_name in model_names]
        for future in as_completed(features):
            result = future.result()
            if result:
                responses.append(result)
 
 #merge the results into 1 response
    merged_result = {
        "viewerid": viewer_id,
        "results": responses
    }

    return merged_result
 

 # HTML form  to make POST requests

@app.route('/post_request.html')
def serve_post_request():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Request Using POST method</title>
        </head>
        <body>
            <h1>POST Request</h1>
            <form action="/recommend" method="POST">
                <label for="viewerid">PLEASE ENTER ONLY THE VIEWER ID:</label>
                <input type="text" id="viewerid" name="viewerid" required>
                <input type="submit" value="Send Request">
            </form>
        </body>
        </html>
    '''

 # Test invoker to check if it is running with GET
@app.route('/test', methods=['GET'])
def test():
    return "Invoker is running", 200


 # Run the Flask application

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

