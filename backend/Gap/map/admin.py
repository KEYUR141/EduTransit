from django.contrib import admin

from .models import (
    AcademicSource,
    Attempt,
    BridgePlan,
    BridgeStep,
    Concept,
    ConceptMapping,
    Curriculum,
    CurriculumConcept,
    DiagnosticItem,
    DiagnosticSession,
    EvidenceChunk,
    LearnerProfile,
    PrerequisiteEdge,
    SupportCase,
    TransitionScenario,
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
    list_display = (
        "prerequisite",
        "dependent",
        "curriculum",
        "approved",
        "reviewed_by",
    )
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
    list_display = (
        "display_name",
        "source_curriculum",
        "destination_curriculum",
        "preferred_language",
    )


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


@admin.register(TransitionScenario)
class TransitionScenarioAdmin(admin.ModelAdmin):
    list_display = (
        "scenario_id",
        "title",
        "education_level",
        "case_type",
        "rarity",
        "review_status",
        "is_active",
    )
    list_filter = ("education_level", "rarity", "review_status", "is_active")
    search_fields = ("scenario_id", "title", "description", "case_type")
    readonly_fields = ("created_at", "updated_at")


class EvidenceChunkInline(admin.TabularInline):
    model = EvidenceChunk
    extra = 0
    fields = ("chunk_id", "section", "approved")
    readonly_fields = ("chunk_id",)


@admin.register(AcademicSource)
class AcademicSourceAdmin(admin.ModelAdmin):
    list_display = ("source_id", "title", "source_type", "review_status")
    list_filter = ("source_type", "review_status")
    search_fields = ("source_id", "title", "organisation")
    inlines = (EvidenceChunkInline,)


@admin.register(EvidenceChunk)
class EvidenceChunkAdmin(admin.ModelAdmin):
    list_display = ("chunk_id", "source", "scenario", "section", "approved")
    list_filter = ("approved", "source__source_type", "source__review_status")
    search_fields = ("chunk_id", "text", "canonical_terms")
    readonly_fields = ("embedding", "checksum", "created_at", "updated_at")
