from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
database = os.getenv("DB")

DATABASE_CONNECTION = f"mysql+pymysql://{user}:{password}@{host}/{database}"