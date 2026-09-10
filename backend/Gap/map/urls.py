from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ConceptViewSet,
    CurriculumViewSet,
    DiagnosticSessionViewSet,
    LearnerProfileViewSet,
    PrerequisiteEdgeViewSet,
    SupportCaseViewSet,
    demo_context,
    health,
)

router = DefaultRouter()
router.register("curricula", CurriculumViewSet, basename="curriculum")
router.register("concepts", ConceptViewSet, basename="concept")
router.register("prerequisite-edges", PrerequisiteEdgeViewSet, basename="prerequisite-edge")
router.register("learners", LearnerProfileViewSet, basename="learner")
router.register("diagnostic-sessions", DiagnosticSessionViewSet, basename="diagnostic-session")
router.register("support-cases", SupportCaseViewSet, basename="support-case")

urlpatterns = [
    path("health/", health, name="health"),
    path("demo-context/", demo_context, name="demo-context"),
    path("", include(router.urls)),
]
