from flask import Flask, request, jsonify
from mem0 import MemoryClient
import os

# Flask app setup
app = Flask(__name__)

# Initialize the Mem0 client
api_key = os.getenv("MEM0_API_KEY", "your_default_api_key")
client = MemoryClient(api_key=api_key)


@app.route('/search_memory', methods=['POST'])
def search_memory():
    """
    Search for specific memories based on a query.
    """
    data = request.json
    user_id = data.get("user_id")
    query = data.get("query")

    if not user_id or not query:
        return jsonify({"error": "user_id and query are required"}), 400

    try:
        response = client.search(query, user_id=user_id)
        return jsonify({"results": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_all_memories', methods=['GET'])
def get_all_memories():
    """
    Retrieve all memories for a specific user.
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        response = client.get_all(user_id=user_id)
        return jsonify({"memories": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_memory', methods=['POST'])
def add_memory():
    """
    Add a new memory for a user.
    """
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")
    categories = data.get("categories", [])

    if not user_id or not content:
        return jsonify({"error": "user_id and content are required"}), 400

    try:
        messages = [
            {"role": "user", "content": content},
            {"role": "assistant", "content": f"I'll remember that: {content}"}
        ]
        response = client.add(messages, user_id=user_id, categories=categories)
        return jsonify({"message": "Memory added successfully", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_memory', methods=['POST'])
def delete_memory():
    """
    Delete a specific memory by ID.
    """
    data = request.json
    memory_id = data.get("memory_id")

    if not memory_id:
        return jsonify({"error": "memory_id is required"}), 400

    try:
        response = client.delete(memory_id)
        return jsonify({"message": "Memory deleted", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_all_memories', methods=['POST'])
def delete_all_memories():
    """
    Delete all memories for a specific user.
    """
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        response = client.delete_all(user_id=user_id)
        return jsonify({"message": "All memories deleted", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user profile memory.
    """
    data = request.json
    user_id = data.get("user_id")
    user_data = data.get("user_data")

    if not user_id or not user_data:
        return jsonify({"error": "user_id and user_data are required"}), 400

    try:
        response = client.add([{"role": "user", "content": user_data}], user_id=user_id)
        return jsonify({"message": "User created with memory", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Ensure the app runs on the correct port for Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
