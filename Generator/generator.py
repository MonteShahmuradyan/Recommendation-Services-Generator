from flask import Flask, request, jsonify                        # import Flask, request and jsonify
import random                                                   # import random to generate random numbers

app = Flask(__name__)                                                # Create a requirement for  Flask

@app.route('/generate', methods=['POST'])                            # Define a method and route to request from generator function
def generate():
    data = request.get_json()                                         #  it use request to get a Json data
    
    model_name = data.get('model_name')                              #It gets 'model_name' from the JSON data                
    viewer_id = data.get('viewerid')                                 # It gets 'model_name' from the JSON data
    
    if not model_name or not viewer_id:                                # Check if 'model_name' and 'viewerid' are provided
        return jsonify({"error": "Missing parameters"}), 400           # Return an error of missing parameters
    
    random_number = random.randint(1, 100)                             # Generate a random number
    
    return jsonify({"reason": model_name, "result": random_number})       # Return a JSON response with 'reason' and 'result'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)      # Debugging is True, open for any host on port 5001



#  curl -X POST http://127.0.0.1:5001/generate -H "Content-Type: application/json" -d "{\"model_name\": \"ModelA\", \"viewerid\": \"123\"}"    


