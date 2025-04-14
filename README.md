# GeoCache-Weather-App

An advanced weather application that auto-detects the user's location using HTML5 Geolocation API and leverages Django's caching framework to optimize performance. This project enhances a simple weather API by integrating geo-location for personalized data and implementing caching for faster load times.

## Table of Contents

- [GeoCache-Weather-App](#geocache-weather-app)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tutorial](#tutorial)
    - [geting a city weather condition from external api](#geting-a-city-weather-condition-from-external-api)
      - [refactoring the request api in another function](#refactoring-the-request-api-in-another-function)
    - [geo location for the current weather](#geo-location-for-the-current-weather)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)

## Overview

The GeoCache-Weather-App is designed to provide an optimized weather experience by:
- Automatically detecting the user's location through the HTML5 Geolocation API.
- Fetching real-time weather data from a weather API (e.g., OpenWeatherMap).
- Using Django's caching framework to temporarily store API responses, reducing load times and API calls.
- Displaying personalized weather information that includes temperature, humidity, conditions, and more.

This project builds upon a simple weather API by adding dynamic geo-location and performance optimizations through caching.

## Features

- **Geo-Location Detection:**  
  Automatically retrieves the user's geographic coordinates using the HTML5 Geolocation API.
  
- **Weather API Integration:**  
  Fetches and displays accurate weather data including temperature, humidity, and conditions.
  
- **Django Caching:**  
  Implements caching strategies to store API responses temporarily, reducing latency and improving overall app performance.
  
- **Responsive Design:**  
  A mobile-friendly interface that adapts to different screen sizes for an optimal user experience.

## Technologies

- **Frontend:** HTML5, CSS, JavaScript  
- **Backend:** Python, Django  
- **APIs:** OpenWeatherMap API (or a similar weather data provider)  
- **Performance:** Django Caching Framework

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AsHkAn-Django/GeoCache-Weather-App-Tutorial.git
   cd GeoCache-Weather-App-Tutorial
2. **Clone the Repository:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use: env\Scripts\activate
    pip install -r requirements.txt
    ```
3. **Configure Environment Variables:**
   
   Create a .env file or set the required environment variables in your system. At a minimum, you might need:
   - DJANGO_SECRET_KEY
   - OPENWEATHERMAP_API_KEY
   - Other environment-specific settings for caching and deployment.

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

## Usage

After installation, the app will:

- Prompt the user to allow location access via the browser.
- Retrieve weather data based on the detected coordinates.
- Display weather information in a clean, responsive layout.
- Use caching to optimize performance by storing frequent API responses for a configurable duration.

## Tutorial
### geting a city weather condition from external api
```python
class GetWeatherView(TemplateView):
    template_name = 'myApp/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('query')
        weather_info = None
        
        if city:
            # Used cacge here for not requesting too much on the api 
            weather_info = cache.get(city)
            
            if not weather_info:
                weather_info = fetch_weather_data(city)
                # keeping this city weather for 5minutes in the cache
                cache.set(city, weather_info, 300)
                if 'error' not in weather_info and not weather_info.get('current'):
                    weather_info = {'error': "City couldn't be found!"}
                        
        context.update({'weather': weather_info,'city': city})
        return context
```

#### refactoring the request api in another function
```python
def fetch_weather_data(city):
    """Fetch weather data from the API."""
    print("nabooooooooddd")
    api_key = env.str('API_KEY')
    try:
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json',
            params={'key': api_key, 'q': city}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"An error occurred: {str(e)}"}
```

### geo location for the current weather

```js
    // Check if the current page is the home page ("/") and if the URL does not already have 'coord'(if you don't do this part the page reloads every second!!)
    if (window.location.pathname === "/" && !window.location.search.includes("coord")) {
      const successCallback = (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
    
        // Redirect to home URL with the coordinates as query parameters
        window.location.href = `/?coord=${lat}&coord=${lng}`;
      };
    
      const errorCallback = (error) => {
        console.log(error);
      };
    
      navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    }
```
```python
#views.py
def receive_coordinates(request):
    """Show the user's current location weather."""
    current_location_weather = None
    city = None
    coords = request.GET.getlist("coord") 
    api_key = env.str('API_KEY')

    if coords and len(coords) == 2:
        lat, lon = coords[0], coords[1]
        # We create a cache_key that includes lat and lon so every cach_key would be unique and if it's not then it's the same location:)
        cache_key = f"weather_{lat}_{lon}"
        # get the weather from the cache
        current_location_weather = cache.get(cache_key)
        if not current_location_weather:
            # only if there isnt availabe in cache, request for external api(optimization) 
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
            try:
                response = response = requests.get(url)
                response.raise_for_status()
                current_location_weather = response.json()
                city = current_location_weather["location"]["name"]
                # keep it in the cache for 5minutes
                cache.set(cache_key, current_location_weather, 300)
            except requests.exceptions.RequestException:
                current_location_weather = None

        if current_location_weather:
            city = current_location_weather.get("location", {}).get("name")
    return render(request, 'myApp/index.html', {'weather':current_location_weather, 'city': city})
```
```python
# and the url in urls.py that is at homepage
path("", receive_coordinates, name="send_coordinates"),
```
---

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

1. **Fork the Repository**
2. **Create a New Branch** (`git checkout -b feature/YourFeature`)
3. **Commit Your Changes** (`git commit -m 'Add some feature'`)
4. **Push to the Branch** (`git push origin feature/YourFeature`)
5. **Open a Pull Request**

Please adhere to the code style and write clear commit messages.


## Acknowledgments

- Special thanks to the developers behind the HTML5 Geolocation API and Django.
- Thanks to the community for providing invaluable resources and support.
