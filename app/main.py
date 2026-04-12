from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, posts, comments, reactions, media, captcha

app = FastAPI(
    title="Mikuro Blog API",
    description="Backend API for Mikuro blog with authentication, posts, comments, and reactions",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(reactions.router, prefix="/api/reactions", tags=["reactions"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(captcha.router, prefix="/api/captcha", tags=["captcha"])

@app.get("/")
async def root():
    return {"message": "Mikuro Blog API"}