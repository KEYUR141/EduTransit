from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Concept,
    Curriculum,
    CurriculumConcept,
    DiagnosticSession,
    LearnerProfile,
    PrerequisiteEdge,
    SupportCase,
)
from .serializers import (
    AnswerSerializer,
    AttemptSerializer,
    BridgePlanSerializer,
    ConceptSerializer,
    CurriculumSerializer,
    DemoContextSerializer,
    DiagnosticItemPublicSerializer,
    DiagnosticSessionSerializer,
    HealthSerializer,
    LearnerProfileSerializer,
    PrerequisiteEdgeSerializer,
    SupportCaseSerializer,
)
from .services import (
    close_if_exhausted,
    generate_bridge_plan,
    next_diagnostic_item,
    record_answer,
)
from .services import (
    gap_map as build_gap_map,
)


class PrototypeAllowAnyMixin:
    """The hackathon demo is open; replace this with role permissions before deployment."""

    permission_classes = [AllowAny]


class CurriculumViewSet(PrototypeAllowAnyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    filterset_fields = ["board", "grade", "subject", "medium", "version"]
    search_fields = ["board", "subject", "medium"]


class ConceptViewSet(PrototypeAllowAnyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    search_fields = ["name", "code", "description"]


class PrerequisiteEdgeViewSet(PrototypeAllowAnyMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PrerequisiteEdgeSerializer
    filterset_fields = ["curriculum", "prerequisite", "dependent", "approved"]

    def get_queryset(self):
        return PrerequisiteEdge.objects.filter(approved=True).select_related(
            "curriculum", "prerequisite", "dependent"
        )


class LearnerProfileViewSet(PrototypeAllowAnyMixin, viewsets.ModelViewSet):
    queryset = LearnerProfile.objects.select_related(
        "source_curriculum", "destination_curriculum"
    )
    serializer_class = LearnerProfileSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]


class DiagnosticSessionViewSet(PrototypeAllowAnyMixin, viewsets.ModelViewSet):
    serializer_class = DiagnosticSessionSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return DiagnosticSession.objects.select_related(
            "learner__source_curriculum",
            "learner__destination_curriculum",
            "target_concept",
        ).prefetch_related("attempts__item__concept")

    def perform_create(self, serializer):
        serializer.save(status="active", completed_at=None)

    @action(detail=True, methods=["get"], url_path="next-question")
    def next_question(self, request, pk=None):
        session = self.get_object()
        item = next_diagnostic_item(session)
        if item is None:
            close_if_exhausted(session)
            session.refresh_from_db(fields=["status", "completed_at"])
        return Response(
            {
                "session_id": session.id,
                "session_status": session.status,
                "completed": item is None,
                "question": DiagnosticItemPublicSerializer(item).data if item else None,
            }
        )

    @action(detail=True, methods=["post"])
    def answer(self, request, pk=None):
        session = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            attempt = record_answer(
                session=session,
                item=serializer.validated_data["item"],
                answer=serializer.validated_data["answer"],
                response_time_ms=serializer.validated_data.get("response_time_ms"),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        session.refresh_from_db(fields=["status", "completed_at"])
        item = next_diagnostic_item(session)
        return Response(
            {
                "attempt": AttemptSerializer(attempt).data,
                "session_status": session.status,
                "completed": item is None,
                "next_question": DiagnosticItemPublicSerializer(item).data if item else None,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get"], url_path="gap-map")
    def gap_map(self, request, pk=None):
        return Response(build_gap_map(self.get_object()))

    @action(detail=True, methods=["post"], url_path="bridge-plan")
    def bridge_plan(self, request, pk=None):
        try:
            plan = generate_bridge_plan(self.get_object())
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(BridgePlanSerializer(plan).data, status=status.HTTP_201_CREATED)


class SupportCaseViewSet(PrototypeAllowAnyMixin, viewsets.ModelViewSet):
    queryset = SupportCase.objects.all()
    serializer_class = SupportCaseSerializer
    filterset_fields = ["category", "status", "is_demo"]
    search_fields = ["reference", "title", "requester_name", "summary"]
    ordering_fields = ["created_at", "updated_at"]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def perform_create(self, serializer):
        serializer.save(status="received", progress_stage=1, is_demo=False)

@extend_schema(responses=HealthSerializer)
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response(
        {
            "status": "ok",
            "service": "GapMap API",
            "time": timezone.now(),
        }
    )


@extend_schema(responses=DemoContextSerializer)
@api_view(["GET"])
@permission_classes([AllowAny])
def demo_context(request):
    """Give the frontend stable discovery data without hard-coded database IDs."""
    learner = LearnerProfile.objects.select_related(
        "source_curriculum", "destination_curriculum"
    ).order_by("id").first()
    if learner is None:
        return Response(
            {"detail": "Run `python manage.py seed_gapmap_demo` first."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    target_ids = (
        CurriculumConcept.objects.filter(
            curriculum=learner.destination_curriculum,
            concept__diagnostic_items__approved=True,
        )
        .values_list("concept_id", flat=True)
        .distinct()
    )
    targets = Concept.objects.filter(id__in=target_ids).order_by("name")
    return Response(
        {
            "learner": LearnerProfileSerializer(learner).data,
            "targets": ConceptSerializer(targets, many=True).data,
            "recommended_target_code": "linear-equations",
        }
    )
