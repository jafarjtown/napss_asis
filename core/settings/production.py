from .base import *
# import dj_database_url
# production specific settings
# DEBUG = False
# other production settings...


DEBUG = False
# DATABASES = {
#     'default': dj_database_url.config(
#         # Replace this value with your local database's connection string.
#         default='postgresql://postgres:postgres@localhost:5432/mysite',
#         conn_max_age=600
#     )
# }
# This production code might break development mode, so we check whether we're in DEBUG mode