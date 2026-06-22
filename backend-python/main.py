from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analysis import router as analysis_router
from routes.upload_pgn import router as pgn_router

app = FastAPI()

# ✅ REGISTER ROUTES
app.include_router(analysis_router)
app.include_router(pgn_router)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)