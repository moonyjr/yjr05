from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'Moscow')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()
        return jsonify({
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        })
    except requests.exceptions.HTTPError as err:
        return jsonify({
            'error': 'Failed to fetch weather data',
            'status_code': response.status_code,
            'details': response.text
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
