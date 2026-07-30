from routers.monthly_summary import router as monthly_summary_router
from routers.transaction import router as transaction_router
from routers.budget import router as budget_router
from routers.savings_tracker import router as savings_tracker_router
from routers.balance import router as balance_router

from fastapi import FastAPI

app = FastAPI(title= "Personal Finance Tracker")

app.include_router(
    balance_router
)

app.include_router(
    transaction_router
)

app.include_router(
    budget_router
)

app.include_router(
    savings_tracker_router
)

app.include_router(
    monthly_summary_router
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

