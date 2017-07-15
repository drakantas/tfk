from sanic.config import LOGGING
from tfk.foundation import bootstrap

app = bootstrap()

LOGGING['loggers']['network']['handlers'] = ['accessTimedRotatingFile', 'errorTimedRotatingFile']


if __name__ == "__main__":
    app.run(host=app.config.HOST, port=app.config.PORT, workers=app.config.WORKERS, log_config=LOGGING, debug=True)
