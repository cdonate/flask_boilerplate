
import os

os.environ.update({
    'APP_SETTINGS': 'app.config.TestingConfig',
    'SECRET_KEY': 'SECRET-KEY',
    'DATABASE_URL': 'postgresql+psycopg2://motors:motors@localhost/motors-test',
    'API-TOKEN': 'nZoX8-iPEns-7hUqw-I2QDq',
})