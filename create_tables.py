from app.database import Base, engine
from app.models import Location

Base.metadata.create_all(bind=engine)

print("Tables created")
