from flask import Flask, request, jsonify, redirect
import random
import string

app = Flask(__name__)

# User data example
users = {
    "user1": {"tier": 1, "urls": {}},
    "user2": {"tier": 2, "urls": {}},
}


# Function to generate a random short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# Endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    user_id = request.json.get('user_id')
    long_url = request.json.get('long_url')

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    user = users[user_id]

    if user['tier'] == 1 and len(user['urls']) >= 1000:
        return jsonify({"error": "Tier 1 user exceeded request limit"}), 403
    elif user['tier'] == 2 and len(user['urls']) >= 100:
        return jsonify({"error": "Tier 2 user exceeded request limit"}), 403

    # Assumes there's a preferred_url key
    preferred_url = request.json.get('preferred_url')

    if preferred_url:
        if preferred_url in user['urls']:
            return jsonify({"error": "Preferred URL already exists"}), 400
        short_url = preferred_url
    else:
        short_url = generate_short_url()

    user['urls'][short_url] = long_url
    return jsonify({"short_url": f"yourdomain.com/{short_url}"})


# Endpoint to get user's URL history
@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    user = users[user_id]
    return jsonify({"urls": user['urls']})


# Redirect short URL to original URL
@app.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    for user in users.values():
        if short_url in user['urls']:
            return redirect(user['urls'][short_url], code=302)

    return jsonify({"error": "Short URL not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
