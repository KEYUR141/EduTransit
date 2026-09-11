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
    embedding_map,
    health,
    rag_retrieve,
)

router = DefaultRouter()
router.register("curricula", CurriculumViewSet, basename="curriculum")
router.register("concepts", ConceptViewSet, basename="concept")
router.register(
    "prerequisite-edges", PrerequisiteEdgeViewSet, basename="prerequisite-edge"
)
router.register("learners", LearnerProfileViewSet, basename="learner")
router.register(
    "diagnostic-sessions", DiagnosticSessionViewSet, basename="diagnostic-session"
)
router.register("support-cases", SupportCaseViewSet, basename="support-case")

urlpatterns = [
    path("health/", health, name="health"),
    path("rag/retrieve/", rag_retrieve, name="rag-retrieve"),
    path("rag/embedding-map/", embedding_map, name="embedding-map"),
    path("demo-context/", demo_context, name="demo-context"),
    path("", include(router.urls)),
]
