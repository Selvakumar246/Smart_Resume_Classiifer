import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.database import Base, engine
from app.db import models

def main():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database recreated successfully!")

if __name__ == "__main__":
    main()
