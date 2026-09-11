from rest_framework import serializers

from .models import (
    Attempt,
    BridgePlan,
    BridgeStep,
    Concept,
    Curriculum,
    CurriculumConcept,
    DiagnosticItem,
    DiagnosticSession,
    LearnerProfile,
    PrerequisiteEdge,
    SupportCase,
)


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = "__all__"


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = "__all__"


class PrerequisiteEdgeSerializer(serializers.ModelSerializer):
    prerequisite_name = serializers.CharField(
        source="prerequisite.name", read_only=True
    )
    dependent_name = serializers.CharField(source="dependent.name", read_only=True)

    class Meta:
        model = PrerequisiteEdge
        fields = "__all__"


class LearnerProfileSerializer(serializers.ModelSerializer):
    source_curriculum_name = serializers.CharField(
        source="source_curriculum.__str__", read_only=True
    )
    destination_curriculum_name = serializers.CharField(
        source="destination_curriculum.__str__", read_only=True
    )

    class Meta:
        model = LearnerProfile
        fields = "__all__"


class DiagnosticItemPublicSerializer(serializers.ModelSerializer):
    concept_name = serializers.CharField(source="concept.name", read_only=True)

    class Meta:
        model = DiagnosticItem
        fields = [
            "id",
            "concept",
            "concept_name",
            "prompt",
            "language",
            "options",
            "difficulty",
        ]


class AttemptSerializer(serializers.ModelSerializer):
    concept = serializers.IntegerField(source="item.concept_id", read_only=True)
    concept_name = serializers.CharField(source="item.concept.name", read_only=True)
    correct_answer = serializers.CharField(source="item.correct_answer", read_only=True)
    explanation = serializers.CharField(source="item.explanation", read_only=True)

    class Meta:
        model = Attempt
        fields = [
            "id",
            "item",
            "concept",
            "concept_name",
            "answer",
            "correct_answer",
            "explanation",
            "is_correct",
            "response_time_ms",
            "created_at",
        ]
        read_only_fields = ["is_correct", "created_at"]


class DiagnosticSessionSerializer(serializers.ModelSerializer):
    learner_name = serializers.CharField(source="learner.display_name", read_only=True)
    target_concept_name = serializers.CharField(
        source="target_concept.name", read_only=True
    )
    attempts = AttemptSerializer(many=True, read_only=True)

    class Meta:
        model = DiagnosticSession
        fields = [
            "id",
            "learner",
            "learner_name",
            "target_concept",
            "target_concept_name",
            "status",
            "max_questions",
            "created_at",
            "completed_at",
            "attempts",
        ]
        read_only_fields = ["status", "created_at", "completed_at", "attempts"]

    def validate(self, attrs):
        learner = attrs.get("learner") or getattr(self.instance, "learner", None)
        target = attrs.get("target_concept") or getattr(
            self.instance, "target_concept", None
        )
        if (
            learner
            and target
            and not CurriculumConcept.objects.filter(
                curriculum=learner.destination_curriculum,
                concept=target,
            ).exists()
        ):
            raise serializers.ValidationError(
                {"target_concept": "This concept is not in the destination curriculum."}
            )
        return attrs


class AnswerSerializer(serializers.Serializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=DiagnosticItem.objects.filter(approved=True), source="item"
    )
    answer = serializers.CharField(max_length=255)
    response_time_ms = serializers.IntegerField(
        min_value=0, required=False, allow_null=True
    )


class BridgeStepSerializer(serializers.ModelSerializer):
    concept_name = serializers.CharField(source="concept.name", read_only=True)
    concept_code = serializers.CharField(source="concept.code", read_only=True)

    class Meta:
        model = BridgeStep
        fields = [
            "id",
            "concept",
            "concept_code",
            "concept_name",
            "order",
            "activity",
            "duration_minutes",
            "evidence_prompt",
            "resource_url",
            "completed",
        ]


class BridgePlanSerializer(serializers.ModelSerializer):
    steps = BridgeStepSerializer(many=True, read_only=True)

    class Meta:
        model = BridgePlan
        fields = [
            "id",
            "session",
            "status",
            "teacher_note",
            "created_at",
            "updated_at",
            "steps",
        ]
        read_only_fields = ["session", "created_at", "updated_at", "steps"]


class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
    time = serializers.DateTimeField()


class DemoContextSerializer(serializers.Serializer):
    learner = LearnerProfileSerializer()
    targets = ConceptSerializer(many=True)
    recommended_target_code = serializers.CharField()


class SupportCaseSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(
        source="get_category_display", read_only=True
    )
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = SupportCase
        fields = [
            "id",
            "reference",
            "title",
            "requester_name",
            "requester_role",
            "category",
            "category_label",
            "summary",
            "source_label",
            "source_location",
            "destination_label",
            "destination_location",
            "status",
            "status_label",
            "progress_stage",
            "matched_scenario",
            "analysis_confidence_score",
            "analysis_confidence_level",
            "review_required",
            "review_route",
            "analysis_snapshot",
            "analysed_at",
            "is_demo",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "reference",
            "status",
            "status_label",
            "progress_stage",
            "matched_scenario",
            "analysis_confidence_score",
            "analysis_confidence_level",
            "review_required",
            "review_route",
            "analysis_snapshot",
            "analysed_at",
            "is_demo",
            "created_at",
            "updated_at",
        ]

    def validate_summary(self, value):
        value = value.strip()
        if len(value) < 15:
            raise serializers.ValidationError(
                "Please describe the situation in at least 15 characters."
            )
        return value


class RagRetrieveRequestSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3, max_length=500)
    scenario_id = serializers.CharField(max_length=12, required=False)
    top_k = serializers.IntegerField(min_value=1, max_value=10, default=5)


class RagCitationSerializer(serializers.Serializer):
    source_id = serializers.CharField()
    title = serializers.CharField()
    organisation = serializers.CharField(allow_blank=True)
    url = serializers.URLField(allow_blank=True)
    version = serializers.CharField(allow_blank=True)
    review_status = serializers.CharField()


class RagRetrievalResultSerializer(serializers.Serializer):
    chunk_id = serializers.CharField()
    score = serializers.FloatField()
    lexical_score = serializers.FloatField()
    vector_score = serializers.FloatField()
    matched_terms = serializers.ListField(child=serializers.CharField())
    retrieval_reasons = serializers.ListField(child=serializers.CharField())
    text = serializers.CharField()
    section = serializers.CharField(allow_blank=True)
    page = serializers.IntegerField(allow_null=True)
    metadata = serializers.DictField()
    citation = RagCitationSerializer()


class RagGuardrailsSerializer(serializers.Serializer):
    scenario_scope_enforced = serializers.BooleanField()
    approved_chunks_only = serializers.BooleanField()
    integrity_checksum_verified = serializers.BooleanField()
    embedding_model_match_enforced = serializers.BooleanField()
    cross_scenario_discovery = serializers.BooleanField()
    maximum_results = serializers.IntegerField()
    model_decision_allowed = serializers.BooleanField()


class RagConfidenceSerializer(serializers.Serializer):
    score = serializers.FloatField()
    level = serializers.ChoiceField(choices=["high", "medium", "low"])
    signal = serializers.CharField()
    top_result_score = serializers.FloatField()
    matched_term_coverage = serializers.FloatField()
    supporting_chunks = serializers.IntegerField()
    discovery_margin = serializers.FloatField()
    explanation = serializers.CharField()
    is_eligibility_probability = serializers.BooleanField()


class RagReviewRouteSerializer(serializers.Serializer):
    required = serializers.BooleanField()
    route = serializers.CharField()
    priority = serializers.CharField()
    reason_codes = serializers.ListField(child=serializers.CharField())
    publication_status = serializers.CharField()


class RagMatchedScenarioSerializer(serializers.Serializer):
    scenario_id = serializers.CharField()
    title = serializers.CharField()
    rarity = serializers.CharField()


class RagRetrieveResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
    scenario_id = serializers.CharField(allow_null=True)
    discovery_mode = serializers.BooleanField()
    matched_scenario = RagMatchedScenarioSerializer(allow_null=True)
    retrieval_mode = serializers.CharField()
    embedding_backend = serializers.CharField()
    confidence = RagConfidenceSerializer()
    review = RagReviewRouteSerializer()
    guardrails = RagGuardrailsSerializer()
    count = serializers.IntegerField()
    results = RagRetrievalResultSerializer(many=True)


class SupportCaseAnalyseRequestSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3, max_length=500, required=False)
    scenario_id = serializers.CharField(max_length=12, required=False)
    top_k = serializers.IntegerField(min_value=1, max_value=10, default=5)


class SupportCaseAnalyseResponseSerializer(serializers.Serializer):
    case = SupportCaseSerializer()
    analysis = RagRetrieveResponseSerializer()
