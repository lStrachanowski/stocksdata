import sys
import os
from sqlalchemy import create_engine
sys.path.append(os.getcwd()+'\\modules\\')
import credentials
engine = create_engine("postgresql://postgres:"+credentials.PASSWORD + "@localhost/" + credentials.DATABASE_NAME,echo = True)
conn = engine.connect()
def test():
    print("test")


