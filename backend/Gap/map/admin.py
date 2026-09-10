from django.contrib import admin

from .models import (
    Attempt,
    BridgePlan,
    BridgeStep,
    Concept,
    ConceptMapping,
    Curriculum,
    CurriculumConcept,
    DiagnosticItem,
    DiagnosticSession,
    LearnerProfile,
    PrerequisiteEdge,
    SupportCase,
)


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("board", "grade", "subject", "medium", "version")
    list_filter = ("board", "grade", "subject", "medium")
    search_fields = ("board", "subject", "medium")


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name", "description")


@admin.register(CurriculumConcept)
class CurriculumConceptAdmin(admin.ModelAdmin):
    list_display = ("curriculum", "concept", "coverage_depth")
    list_filter = ("curriculum",)
    search_fields = ("concept__name", "local_term", "learning_outcome")


@admin.register(PrerequisiteEdge)
class PrerequisiteEdgeAdmin(admin.ModelAdmin):
    list_display = ("prerequisite", "dependent", "curriculum", "approved", "reviewed_by")
    list_filter = ("curriculum", "approved")
    list_editable = ("approved",)


@admin.register(ConceptMapping)
class ConceptMappingAdmin(admin.ModelAdmin):
    list_display = (
        "source_curriculum",
        "destination_curriculum",
        "source_concept",
        "destination_concept",
        "relation",
        "confidence",
        "approved",
    )
    list_filter = ("relation", "approved")


@admin.register(DiagnosticItem)
class DiagnosticItemAdmin(admin.ModelAdmin):
    list_display = ("concept", "curriculum", "language", "difficulty", "approved")
    list_filter = ("curriculum", "language", "difficulty", "approved")
    list_editable = ("approved",)
    search_fields = ("prompt", "concept__name")


@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "source_curriculum", "destination_curriculum", "preferred_language")


class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0
    readonly_fields = ("item", "answer", "is_correct", "response_time_ms", "created_at")


@admin.register(DiagnosticSession)
class DiagnosticSessionAdmin(admin.ModelAdmin):
    list_display = ("learner", "target_concept", "status", "created_at", "completed_at")
    list_filter = ("status", "target_concept")
    inlines = (AttemptInline,)


class BridgeStepInline(admin.TabularInline):
    model = BridgeStep
    extra = 0


@admin.register(BridgePlan)
class BridgePlanAdmin(admin.ModelAdmin):
    list_display = ("session", "status", "updated_at")
    list_filter = ("status",)
    inlines = (BridgeStepInline,)

@admin.register(SupportCase)
class SupportCaseAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "title",
        "requester_name",
        "category",
        "status",
        "progress_stage",
        "updated_at",
    )
    list_filter = ("category", "status", "is_demo")
    search_fields = ("reference", "title", "requester_name", "summary")
    readonly_fields = ("reference", "created_at", "updated_at")
