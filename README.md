Hello!  This is a simple flask app that tells you the weather!  It requires an API key from openweathermap for weather information, and another one from waqi.info for air quality information (optional).  I'm not using the openweathermap air quality information because it does not use the commonly used scale.  Anyway, it's a flask app and a gunicorn server.  For configuration, please change the `sample_env` file to `.env`, and update the information in it to your liking.  The `gunicorn_starter.sh` may need to be adjusted as well for your particular network.  When you `curl` the app via terminal, it will give you a prettytable output of the information.  Via browser, it shows a subpar table with no borders; I'll get to it eventually.  That is done by checking for a curl user-agent.  The app uses the user's public IP address to determine location, and provides weather information based on that.  You can also add location and change units via url parameters, like this: `0.0.0.0:5000?location=Chicago&units=metric`.