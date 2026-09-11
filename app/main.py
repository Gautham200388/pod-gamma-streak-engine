from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.models import UserProfile
from app.streak import update_streak
from app.badges import award_milestone_badge

app = FastAPI(
    title="CyBreach Pod Gamma API Gateway",
    version="1.0.0",
    description="Track 2 API and Endpoint Gateway",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ScoreInputItem(BaseModel):
    client_id: str = Field(min_length=3, max_length=50)
    security_score: float = Field(ge=0.0, le=100.0)


class StreamAnalyticsPayload(BaseModel):
    metrics: List[ScoreInputItem] = Field(default_factory=list)


class StreakVerificationPayload(BaseModel):
    previous_login_timestamp: str
    current_login_timestamp: str
    active_streak: int = Field(ge=0)


def seed_corporate_profiles() -> List[dict]:
    return [
        {
            "client_id": f"CORP-{index:03d}",
            "company_name": f"Synthetic Corporation {index:03d}",
            "security_score": float(50 + (index * 7) % 51),
        }
        for index in range(1, 51)
    ]


SYNTHETIC_PROFILES = seed_corporate_profiles()

USERS = {
    "demo-user": UserProfile(
        user_id="demo-user",
        current_streak=7,
        last_completion_time=datetime.now() - timedelta(hours=24),
        verified_activity_time=datetime.now() - timedelta(hours=24),
    )
}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/v1/analytics")
async def analytics(payload: StreamAnalyticsPayload):
    metrics = payload.metrics

    if not metrics:
        metrics = [
            ScoreInputItem(
                client_id=profile["client_id"],
                security_score=profile["security_score"],
            )
            for profile in SYNTHETIC_PROFILES
        ]

    average_score = sum(
        item.security_score for item in metrics
    ) / len(metrics)

    return {
        "status": "processed",
        "records_processed": len(metrics),
        "average_security_score": round(average_score, 2),
        "metrics": [item.model_dump() for item in metrics],
    }


@app.post("/api/v1/streaks")
async def verify_streak(payload: StreakVerificationPayload):
    try:
        previous_login = datetime.fromisoformat(
            payload.previous_login_timestamp.replace("Z", "+00:00")
        )
        current_login = datetime.fromisoformat(
            payload.current_login_timestamp.replace("Z", "+00:00")
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format"
        )

    user = UserProfile(
        user_id="api-user",
        current_streak=payload.active_streak,
        last_completion_time=previous_login,
        verified_activity_time=previous_login,
    )

    updated_user = update_streak(user, current_login)

    return {
        "status": "processed",
        "previous_active_streak": payload.active_streak,
        "verified_streak": updated_user.current_streak,
        "last_completion_time": updated_user.last_completion_time,
        "verified_activity_time": updated_user.verified_activity_time,
    }
@app.get("/user/{user_id}/streak")
async def get_user_streak(user_id: str):
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "current_streak": user.current_streak,
        "last_completion_time": user.last_completion_time,
        "verified_activity_time": user.verified_activity_time,
    }

@app.get("/user/{user_id}/badges")
async def get_user_badges(user_id: str):
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    award_milestone_badge(user)

    return {
        "user_id": user.user_id,
        "current_streak": user.current_streak,
        "badges": user.badges,
    }