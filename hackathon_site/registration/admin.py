from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from registration.models import Application, Team as TeamApplied


class ApplicationInline(admin.TabularInline):
    model = Application
    autocomplete_fields = ("user",)
    extra = 0


@admin.register(TeamApplied)
class TeamAppliedAdmin(admin.ModelAdmin):
    search_fields = ("id", "team_code")
    list_display = ("team_code", "get_members_count")
    inlines = (ApplicationInline,)

    def get_members_count(self, obj):
        return obj.applications.count()

    get_members_count.short_description = "Members"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("applications")


class ApplicationResource(resources.ModelResource):
    class Meta:
        model = Application

        fields = (
            "user__first_name",
            "user__last_name",
            "user__email",
            "team__team_code",
            "birthday",
            "gender",
            "ethnicity",
            "school",
            "study_level",
            "graduation_year",
            "review__status",
            "rsvp",
            "created_at",
            "updated_at",
        )
        export_order = (
            "user__first_name",
            "user__last_name",
            "user__email",
            "team__team_code",
            "birthday",
            "gender",
            "ethnicity",
            "school",
            "study_level",
            "graduation_year",
            "review__status",
            "rsvp",
            "created_at",
            "updated_at",
        )


@admin.register(Application)
class ApplicationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ApplicationResource
    autocomplete_fields = ("user", "team")
    list_display = ("get_full_name", "team", "school")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "team__team_code",
    )
    list_filter = ("school",)

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_full_name.short_description = "User"
