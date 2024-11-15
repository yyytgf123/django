from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API 설정
OPENWEATHER_API_KEY = "Key"  # 발급받은 API 키 적용

# 날씨에 따른 노래 추천 데이터
SONG_RECOMMENDATIONS = {
    "Clear": ["Here Comes the Sun - The Beatles", "Walking on Sunshine - Katrina & The Waves"],
    "Rain": ["Raindrops Keep Fallin' On My Head - B.J. Thomas", "Set Fire to the Rain - Adele"],
    "Clouds": ["Cloudy Day - Tones And I", "Both Sides Now - Joni Mitchell"],
    "Snow": ["Let It Snow! Let It Snow! Let It Snow! - Dean Martin"],
    "Default": ["What a Wonderful World - Louis Armstrong"]
}

def get_weather(city):
    """OpenWeatherMap API를 통해 날씨 정보 가져오기"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    # 응답 상태 코드와 JSON 데이터 확인 (디버깅용)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        return weather, temperature
    return None, None

def get_songs_by_weather(weather):
    """날씨에 따른 노래 추천"""
    return SONG_RECOMMENDATIONS.get(weather, SONG_RECOMMENDATIONS["Default"])

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    temperature = None
    songs = []
    city = None

    if request.method == "POST":
        city = request.form.get("city")  # 사용자가 입력한 도시 이름
        weather, temperature = get_weather(city)
        if weather:
            songs = get_songs_by_weather(weather)

    return render_template("index.html", city=city, weather=weather, temperature=temperature, songs=songs)

if __name__ == "__main__":
    app.run(debug=True)
