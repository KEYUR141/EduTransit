# GapMap Backend Prototype

This Django REST API implements the demo's complete decision path: discover a learner transition, start a target-topic diagnostic, select the next question adaptively, expose the evidence as a concept gap map, and generate an ordered bridge plan.

## Run locally

From the `SIH2026` repository root:

```powershell
.\env\Scripts\Activate.ps1
cd backend\Gap
python manage.py migrate
python manage.py seed_gapmap_demo
python manage.py runserver
```

Open:

- API discovery: `http://127.0.0.1:8000/api/`
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Django admin: `http://127.0.0.1:8000/admin/`
- Health check: `http://127.0.0.1:8000/api/health/`

## Frontend support-request connection

The React dashboard checks GET /api/health/, loads the active workspace through GET /api/support-cases/, and creates requests through POST /api/support-cases/.

The frontend defaults to http://127.0.0.1:8000/api. Override it with VITE_API_BASE_URL in frontend/.env; see frontend/.env.example.

## Demo API journey

1. `GET /api/demo-context/` discovers the seeded learner and valid target concepts.
2. `POST /api/diagnostic-sessions/` with `learner`, `target_concept`, and `max_questions` starts a diagnostic.
3. `GET /api/diagnostic-sessions/{id}/next-question/` returns a question without exposing its answer.
4. `POST /api/diagnostic-sessions/{id}/answer/` records evidence and returns the adaptive next question.
5. `GET /api/diagnostic-sessions/{id}/gap-map/` returns nodes and prerequisite edges for visualization.
6. `POST /api/diagnostic-sessions/{id}/bridge-plan/` returns ordered learning activities and reassessment prompts.

Example session request:

```json
{
  "learner": 1,
  "target_concept": 5,
  "max_questions": 6
}
```

Use `/api/demo-context/` instead of hard-coding these example IDs in the frontend.

## Why the prototype is credible

- Only approved questions and prerequisite edges affect decisions.
- The diagnostic walks backward from the classroom target when an answer exposes a gap.
- Preferred-language questions are selected first, with another language as fallback.
- Mastery output includes probability and evidence count; it is not a hidden AI verdict.
- Bridge steps contain an activity, time estimate, and observable evidence prompt.
- AI can later suggest curriculum mappings or explanations, but teacher approval remains the publishing boundary.

## Database

SQLite is the default so the demo runs without setup. To use PostgreSQL, copy `.env.example` to `.env` and set `DATABASE_URL`.

## Verification

```powershell
python manage.py check
python manage.py test map -v 2
python manage.py spectacular --file schema.yml --validate
```

The API is intentionally open for the local hackathon demo. Add authentication and student/teacher role permissions before any real deployment.
