"""
Flask Frontend Application for Financial Advisor
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import requests
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/api")


def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_auth_headers():
    """Get authentication headers for API requests."""
    return {
        'Authorization': f"Bearer {session.get('token', '')}",
        'Content-Type': 'application/json'
    }


# Authentication Routes
@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": data['email'], "password": data['password']},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                session['token'] = result['access_token']
                session['user'] = result['user']['email']
                session['user_name'] = result['user'].get('full_name', data['email'])
                session.permanent = True
                return jsonify({"success": True, "message": "Login successful"})
            else:
                error_msg = "Invalid credentials"
                try:
                    error_msg = response.json().get('detail', error_msg)
                except:
                    pass
                return jsonify({"success": False, "message": error_msg}), 401
        except requests.exceptions.ConnectionError:
            return jsonify({"success": False, "message": "Cannot connect to backend server"}), 500
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "email": data['email'],
                    "password": data['password'],
                    "full_name": data['full_name']
                },
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                session['token'] = result['access_token']
                session['user'] = result['user']['email']
                session['user_name'] = result['user'].get('full_name', data['email'])
                session.permanent = True
                return jsonify({"success": True, "message": "Registration successful"})
            else:
                error_detail = "Registration failed"
                try:
                    error_detail = response.json().get('detail', error_detail)
                except:
                    pass
                return jsonify({"success": False, "message": error_detail}), response.status_code
        except requests.exceptions.ConnectionError:
            return jsonify({"success": False, "message": "Cannot connect to backend server"}), 500
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


# Protected Routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('user'), user_name=session.get('user_name'))


@app.route('/portfolio')
@login_required
def portfolio():
    return render_template('portfolio.html', user=session.get('user'))


@app.route('/goals')
@login_required
def goals():
    return render_template('goals.html', user=session.get('user'))


@app.route('/budget')
@login_required
def budget():
    return render_template('budget.html', user=session.get('user'))


@app.route('/recommendations')
@login_required
def recommendations():
    return render_template('recommendations.html', user=session.get('user'))


@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=session.get('user'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=session.get('user'))


@app.route('/market')
@login_required
def market():
    return render_template('market.html', user=session.get('user'))


@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', user=session.get('user'))


# API Proxy endpoints
@app.route('/api/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(endpoint):
    """Proxy API requests to the backend with authentication."""
    # Allow login and register without token
    if endpoint in ['auth/login', 'auth/register']:
        headers = {'Content-Type': 'application/json'}
    else:
        if 'token' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        headers = get_auth_headers()

    url = f"{API_URL}/{endpoint}"

    try:
        if request.method == 'GET':
            response = requests.get(url, headers=headers, params=request.args, timeout=30)
        elif request.method == 'POST':
            response = requests.post(url, headers=headers, json=request.get_json(), timeout=30)
        elif request.method == 'PUT':
            response = requests.put(url, headers=headers, json=request.get_json(), timeout=30)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)

        # Try to return JSON response
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": response.text}), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to backend server. Make sure the FastAPI server is running."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Health check endpoint
@app.route('/health')
def health():
    """Health check for the Flask frontend."""
    backend_status = "unknown"
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            backend_status = "healthy"
        else:
            backend_status = "degraded"
    except:
        backend_status = "unavailable"

    return jsonify({
        "frontend": "healthy",
        "backend": backend_status
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
