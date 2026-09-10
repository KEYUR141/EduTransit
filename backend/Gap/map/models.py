import uuid

from django.core.exceptions import ValidationError
from django.db import models


class Curriculum(models.Model):
    board = models.CharField(max_length=120)
    grade = models.PositiveSmallIntegerField()
    subject = models.CharField(max_length=80)
    medium = models.CharField(max_length=80)
    version = models.CharField(max_length=40, default="2026")
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["board", "grade", "subject", "medium"]
        constraints = [
            models.UniqueConstraint(
                fields=["board", "grade", "subject", "medium", "version"],
                name="unique_curriculum_version",
            )
        ]

    def __str__(self):
        return f"{self.board} Grade {self.grade} {self.subject} ({self.medium})"


class Concept(models.Model):
    code = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CurriculumConcept(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="curriculum_concepts"
    )
    concept = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="curriculum_entries"
    )
    local_term = models.CharField(max_length=160, blank=True)
    learning_outcome = models.TextField(blank=True)
    coverage_depth = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "concept"], name="unique_concept_per_curriculum"
            )
        ]

    def __str__(self):
        return f"{self.curriculum}: {self.concept}"


class PrerequisiteEdge(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="prerequisite_edges"
    )
    prerequisite = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="supports_concepts"
    )
    dependent = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="requires_concepts"
    )
    rationale = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    reviewed_by = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "prerequisite", "dependent"],
                name="unique_prerequisite_edge",
            )
        ]

    def clean(self):
        if self.prerequisite_id == self.dependent_id:
            raise ValidationError("A concept cannot be its own prerequisite.")

    def __str__(self):
        return f"{self.prerequisite} -> {self.dependent}"


class ConceptMapping(models.Model):
    RELATIONS = [
        ("equivalent", "Equivalent"),
        ("partial", "Partial overlap"),
        ("missing", "Missing from source"),
    ]

    source_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="outgoing_mappings"
    )
    destination_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="incoming_mappings"
    )
    source_concept = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="source_mappings", null=True, blank=True
    )
    destination_concept = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="destination_mappings"
    )
    relation = models.CharField(max_length=20, choices=RELATIONS)
    confidence = models.DecimalField(max_digits=4, decimal_places=3, default=0.500)
    rationale = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.source_curriculum} to {self.destination_curriculum}: {self.destination_concept}"


class DiagnosticItem(models.Model):
    LANGUAGES = [("en", "English"), ("hi", "Hindi")]

    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="diagnostic_items"
    )
    concept = models.ForeignKey(
        Concept, on_delete=models.CASCADE, related_name="diagnostic_items"
    )
    prompt = models.TextField()
    language = models.CharField(max_length=8, choices=LANGUAGES, default="en")
    options = models.JSONField(default=list)
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)
    difficulty = models.PositiveSmallIntegerField(default=1)
    approved = models.BooleanField(default=False)
    source_reference = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["concept", "difficulty", "id"]

    def __str__(self):
        return f"{self.concept} ({self.language})"


class LearnerProfile(models.Model):
    display_name = models.CharField(max_length=120)
    source_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.PROTECT, related_name="source_learners"
    )
    destination_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.PROTECT, related_name="destination_learners"
    )
    preferred_language = models.CharField(max_length=8, default="hi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class DiagnosticSession(models.Model):
    STATUSES = [
        ("active", "Active"),
        ("review", "Teacher review"),
        ("complete", "Complete"),
    ]

    learner = models.ForeignKey(
        LearnerProfile, on_delete=models.CASCADE, related_name="diagnostic_sessions"
    )
    target_concept = models.ForeignKey(
        Concept, on_delete=models.PROTECT, related_name="targeted_sessions"
    )
    status = models.CharField(max_length=16, choices=STATUSES, default="active")
    max_questions = models.PositiveSmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.learner}: {self.target_concept}"


class Attempt(models.Model):
    session = models.ForeignKey(
        DiagnosticSession, on_delete=models.CASCADE, related_name="attempts"
    )
    item = models.ForeignKey(DiagnosticItem, on_delete=models.PROTECT)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(fields=["session", "item"], name="one_attempt_per_item")
        ]

    def __str__(self):
        return f"{self.session}: {self.item}"


class BridgePlan(models.Model):
    STATUSES = [("draft", "Draft"), ("approved", "Approved"), ("complete", "Complete")]

    session = models.OneToOneField(
        DiagnosticSession, on_delete=models.CASCADE, related_name="bridge_plan"
    )
    status = models.CharField(max_length=16, choices=STATUSES, default="draft")
    teacher_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bridge plan for {self.session}"


class BridgeStep(models.Model):
    plan = models.ForeignKey(BridgePlan, on_delete=models.CASCADE, related_name="steps")
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    order = models.PositiveSmallIntegerField()
    activity = models.TextField(blank=True)
    duration_minutes = models.PositiveSmallIntegerField(default=20)
    evidence_prompt = models.TextField(blank=True)
    resource_url = models.URLField(blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["plan", "concept"], name="unique_concept_per_plan"),
            models.UniqueConstraint(fields=["plan", "order"], name="unique_order_per_plan"),
        ]

    def __str__(self):
        return f"{self.order}. {self.concept}"

def create_support_reference():
    return f"GM-{uuid.uuid4().hex[:8].upper()}"


class SupportCase(models.Model):
    REQUESTER_ROLES = [
        ("student", "Student"),
        ("parent", "Parent or guardian"),
        ("educator", "Educator or counsellor"),
    ]
    CATEGORIES = [
        ("school-change", "School or board change"),
        ("language", "Language difficulty"),
        ("learning-break", "Learning interruption"),
        ("higher-education", "College or programme change"),
        ("study-abroad", "Study-abroad preparation"),
        ("unsure", "Not yet classified"),
    ]
    STATUSES = [
        ("received", "Request received"),
        ("evidence_review", "Evidence review"),
        ("gap_analysis", "Gap comparison"),
        ("roadmap", "Support roadmap"),
        ("readiness_review", "Readiness review"),
    ]

    reference = models.CharField(
        max_length=16, unique=True, default=create_support_reference, editable=False
    )
    title = models.CharField(max_length=180, blank=True)
    requester_name = models.CharField(max_length=120, blank=True)
    requester_role = models.CharField(
        max_length=20, choices=REQUESTER_ROLES, default="student"
    )
    category = models.CharField(max_length=32, choices=CATEGORIES)
    summary = models.TextField()
    source_label = models.CharField(max_length=180, blank=True)
    source_location = models.CharField(max_length=100, blank=True)
    destination_label = models.CharField(max_length=180, blank=True)
    destination_location = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=24, choices=STATUSES, default="received")
    progress_stage = models.PositiveSmallIntegerField(default=1)
    is_demo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.reference}: {self.title or self.get_category_display()}"
