import os

DEBUG = int(os.environ.get("DEBUG", default=0))
OUTPUT_TEST = int(os.environ.get("OUTPUT_TEST", default=0))
ENVIRONMENT = os.environ.get("ENVIRONMENT", default="development")

AUTH_ACCESS = os.environ.get("AUTH_ACCESS", default="")

DATABASE_TYPE = os.environ.get("DATABASE_TYPE", default="postgresql")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", default="postgres")
PASSWORD = os.environ.get("PASSWORD", default="postgres")
HOSTNAME = os.environ.get("HOSTNAME", default="localhost")
# DATABASE_HOSTNAME = os.environ.get("HOSTNAME", default="192.168.56.1") # moj ip
DATABASE = os.environ.get("DATABASE", default="matija")

# DB_ACCESS = 'postgresql://postgres:postgres@localhost/matija'

DB_ACCESS = f"{DATABASE_TYPE}://{DATABASE_USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}"
print('xxx',DB_ACCESS)

# DB_ACCESS = f"{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@192.168.56.1/{DATABASE}"

