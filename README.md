# Pod Gamma Streak Engine

A Python-based streak tracking and milestone badge system built for the Pod Gamma assignment.

## Features

- Track user streaks
- Ignore duplicate completions within 24 hours
- Increase streaks between 24–48 hours
- Reset streaks after 48 hours
- Award milestone badges
- Prevent duplicate badge awards
- Automated testing using Pytest
- Time simulation using Freezegun

## Project Structure

```
pod-gamma-streak-engine/
│
├── app/
│   ├── models.py
│   ├── streak.py
│   ├── badges.py
│   └── __init__.py
│
├── tests/
│   ├── test_streak.py
│   └── __init__.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

- Python 3.12
- Pydantic
- Pytest
- Freezegun
- Git

## Installation

```bash
git clone <repository-url>
cd pod-gamma-streak-engine

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
```

Expected output:

```
7 passed
```

## Future Improvements

- More badge milestones
- Database integration
- REST API using FastAPI
- User authentication
- Persistent storage