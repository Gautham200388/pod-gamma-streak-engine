from app.models import UserProfile


MILESTONE_BADGES = {
    7: "badge_7_day_streak",
    30: "badge_30_day_streak",
    100: "badge_100_day_streak",
}


def award_milestone_badge(user: UserProfile) -> UserProfile:
    badge_id = MILESTONE_BADGES.get(user.current_streak)

    if badge_id is not None and badge_id not in user.badges:
        user.badges.append(badge_id)

    return user