from fastapi import FastAPI
from app.routes import auth

# Import all models so SQLAlchemy can resolve relationships
from app.models import user, event, ticket, order, escrow, token_blacklist

app = FastAPI()

app.include_router(auth.router)
