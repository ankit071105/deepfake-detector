import secrets
print(secrets.token_hex(32))

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
app.secret_key = os.environ['8a688084a95cdfac893e9b48506e238b15036f46120b2c330d71cea1002f27fd']