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
    prerequisite_name = serializers.CharField(source="prerequisite.name", read_only=True)
    dependent_name = serializers.CharField(source="dependent.name", read_only=True)

    class Meta:
        model = PrerequisiteEdge
        fields = "__all__"


class LearnerProfileSerializer(serializers.ModelSerializer):
    source_curriculum_name = serializers.CharField(source="source_curriculum.__str__", read_only=True)
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
    target_concept_name = serializers.CharField(source="target_concept.name", read_only=True)
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
        target = attrs.get("target_concept") or getattr(self.instance, "target_concept", None)
        if learner and target and not CurriculumConcept.objects.filter(
            curriculum=learner.destination_curriculum,
            concept=target,
        ).exists():
            raise serializers.ValidationError(
                {"target_concept": "This concept is not in the destination curriculum."}
            )
        return attrs



class AnswerSerializer(serializers.Serializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=DiagnosticItem.objects.filter(approved=True), source="item"
    )
    answer = serializers.CharField(max_length=255)
    response_time_ms = serializers.IntegerField(min_value=0, required=False, allow_null=True)


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
    category_label = serializers.CharField(source="get_category_display", read_only=True)
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
            "is_demo",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "reference",
            "status",
            "status_label",
            "progress_stage",
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
