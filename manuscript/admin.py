from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from manuscript.models import (
    AuthorityFile,
    Codex,
    Detail,
    EditorialStatus,
    Folio,
    Library,
    LineCode,
    Location,
    LocationAlias,
    Reference,
    SingleManuscript,
    Stanza,
    StanzaTranslated,
    StanzaVariant,
    TextDecoration,
    ViewerNote,
)
from manuscript.resources import (
    EditorialStatusResource,
    ReferenceResource,
    SingleManuscriptResource,
    FolioResource,
    LocationResource,
    LocationAliasResource,
    LineCodeResource,
)
from textannotation.models import TextAnnotation


# Inline models --------------------------------------------
class StanzaInline(admin.StackedInline):
    model = Stanza
    extra = 1
    fields = (
        "stanza_line_code_starts",
        "stanza_line_code_ends",
        "stanza_text",
        "stanza_notes",
        "add_stanza_variant_link",
        "display_stanza_variants",
    )
    readonly_fields = (
        "add_stanza_variant_link",
        "display_stanza_variants",
    )

    def add_stanza_variant_link(self, obj):
        url = reverse("admin:manuscript_stanzavariant_add") + "?stanza=" + str(obj.id)
        return format_html('<a href="{}">Add Stanza Variant</a>', url)

    add_stanza_variant_link.short_description = "Add Stanza Variant"

    def display_stanza_variants(self, obj):
        variants = ["- {}".format(variant) for variant in obj.stanzavariant_set.all()]
        return format_html("<br>".join(variants))

    display_stanza_variants.short_description = "Stanza Variants"


class StanzaVariantInline(admin.StackedInline):
    model = StanzaVariant
    extra = 1


class FolioInline(admin.StackedInline):
    model = Folio
    classes = ("collapse",)
    extra = 1


class DetailInline(admin.StackedInline):
    model = Detail
    classes = ("collapse",)
    extra = 1
    max_num = 1


class TextDecorationInline(admin.StackedInline):
    model = TextDecoration
    classes = ("collapse",)
    extra = 1
    max_num = 1


class ReferenceInline(admin.StackedInline):
    model = Reference
    classes = ("collapse",)
    extra = 1


class EditorialStatusInline(admin.StackedInline):
    model = EditorialStatus
    classes = ("collapse",)
    extra = 1
    max_num = 1


class ViewerNotesInline(admin.StackedInline):
    model = ViewerNote
    classes = ("collapse",)
    extra = 1


class CodexInline(admin.StackedInline):
    model = Codex
    classes = ("collapse",)
    extra = 1
    max_num = 1


class LocationAliasInline(admin.TabularInline):
    model = LocationAlias
    extra = 1


class AuthorityFileInline(admin.TabularInline):
    model = AuthorityFile
    extra = 1


class TextAnnotationInline(GenericTabularInline):
    model = TextAnnotation
    extra = 0
    fields = ("selected_text", "annotation", "annotation_type")
    readonly_fields = ("selected_text",)


# Custom admin models --------------------------------------------
class SingleManuscriptAdmin(ImportExportModelAdmin):
    inlines = [
        AuthorityFileInline,
        TextDecorationInline,
        ReferenceInline,
        DetailInline,
        CodexInline,
        ViewerNotesInline,
        EditorialStatusInline,
        FolioInline,
        TextAnnotationInline,
    ]
    list_display = (
        "siglum",
        "shelfmark",
        "library",
        "manuscript_lost",
        "manuscript_destroyed",
        "has_iiif_url",
        "item_id",
    )
    search_fields = ("siglum",)
    resource_class = SingleManuscriptResource

    @admin.display(boolean=True, description="IIIF Available")
    def has_iiif_url(self, obj):
        return bool(obj.iiif_url)

    class Media:
        js = ("js/text_annotator.js",)
        css = {"all": ("css/text_annotator.css",)}


class FolioAdmin(ImportExportModelAdmin):
    resource_class = FolioResource

    list_display = ["manuscript", "folio_number", "line_range_display", "stanza_count"]
    list_filter = ["manuscript"]
    search_fields = [
        "folio_number",
        "manuscript__siglum",
        "line_code_range_start",
        "line_code_range_end",
    ]

    readonly_fields = ["stanza_list", "line_range_display", "stanza_count"]

    fieldsets = (
        ("Folio Information", {"fields": ("manuscript", "folio_number")}),
        (
            "Line Range",
            {
                "fields": (
                    "line_code_range_start",
                    "line_code_range_end",
                    "line_range_display",
                )
            },
        ),
        (
            "Associated Stanzas",
            {
                "fields": ("stanza_count", "stanza_list"),
            },
        ),
    )

    def stanza_count(self, obj):
        return obj.stanzas.count()

    stanza_count.short_description = "Number of Stanzas"

    def line_range_display(self, obj):
        end = obj.line_code_range_end or "End"
        return f"{obj.line_code_range_start} → {end}"

    line_range_display.short_description = "Line Range"

    def stanza_list(self, obj):
        stanzas = obj.stanzas.order_by("stanza_line_code_starts")
        if not stanzas.exists():
            return "No stanzas associated"

        html = ['<div style="max-height: 400px; overflow-y: auto;">']
        html.append('<table style="width: 100%;">')
        html.append("<tr><th>Line Code</th><th>Text Preview</th></tr>")

        for stanza in stanzas:
            preview = (
                stanza.stanza_text[:100] + "..."
                if len(stanza.stanza_text) > 100
                else stanza.stanza_text
            )
            html.append(
                f"<tr>"
                f'<td style="padding: 5px; border-bottom: 1px solid #eee;">{stanza.stanza_line_code_starts}</td>'
                f'<td style="padding: 5px; border-bottom: 1px solid #eee;">{preview}</td>'
                f"</tr>"
            )

        html.append("</table></div>")
        return format_html("".join(html))

    stanza_list.short_description = "Stanzas on this Folio"

    def has_add_permission(self, request):
        """Disable manual adding - folios should be created via import"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion but with a warning"""
        return True  # You might want to add a custom deletion warning/confirmation


# class FolioAdmin(ImportExportModelAdmin):
#     inlines = [
#         StanzaInline,
#     ]
#     list_filter = ("manuscript",)
#     list_display = (
#         "folio_number",
#         "manuscript",
#     )
#     search_fields = (
#         "folio_number",
#         "manuscript__siglum",
#     )
#     resource_class = FolioResource
#
#     def add_link_to_edit_stanzas(self, obj):
#         url = reverse("admin:manuscript_stanza_add") + "?folio=" + str(obj.id)
#         return format_html('<a href="{}">Add Stanza</a>', url)
#
#     def manuscript(self, obj):
#         url = reverse(
#             "admin:manuscript_singlemanuscript_change", args=[obj.singlemanuscript.id]
#         )
#         return format_html('<a href="{}">{}</a>', url, obj.singlemanuscript.siglum)
#


class ReferenceAdmin(ImportExportModelAdmin):
    list_display = ("reference", "bert")
    resource_class = ReferenceResource


class LibraryAdmin(admin.ModelAdmin):
    list_display = ("library", "city", "id")
    list_filter = ("city",)


# class EditorialStatusAdmin(admin.ModelAdmin):
#     list_display = ("editorial_priority", "spatial_priority")
#     resource_class = EditorialStatusResource


class CodexAdmin(admin.ModelAdmin):
    list_display = ("id", "support", "height", "folia", "date")


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = (
        "placename_id",
        "name",
        "get_placename_modern",
        "get_mss_placename",
        "toponym_type",
        "place_type",
        "get_related_folios",
        "id",
    )
    search_fields = ("placename_id", "description", "modern_country")
    list_filter = ("place_type", "modern_country", "toponym_type")
    inlines = [LocationAliasInline]

    def description_html(self, obj):
        return format_html(obj.description) if obj.description else ""

    description_html.short_description = "Description"

    def get_related_folios(self, obj):
        return ", ".join([str(folio.folio_number) for folio in obj.folio_set.all()])

    get_related_folios.short_description = "Related folio"

    def get_placename_modern(self, obj):
        alias = LocationAlias.objects.filter(location=obj).first()
        return alias.placename_modern if alias else None

    get_placename_modern.short_description = "Modern Placename"

    def get_mss_placename(self, obj):
        alias = LocationAlias.objects.filter(location=obj).first()
        return alias.placename_from_mss if alias else None

    get_mss_placename.short_description = "Manuscript Placename"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.geocode()


@admin.register(LocationAlias)
class LocationAliasAdmin(ImportExportModelAdmin):
    resource_class = LocationAliasResource
    list_display = (
        "location",
        "placename_alias",
        "show_on_page",
        "placename_from_mss",
        "placename_ancient",
        "placename_standardized",
        # "folio",
        # "manuscript",
    )
    list_filter = ("location",)
    search_fields = ("placename_alias",)
    raw_id_fields = ("location",)


@admin.action(description="Set language of the selected stanza to Italian")
def set_language_to_italian(modeladmin, request, queryset):
    queryset.update(language="it")


@admin.action(description="Set language of the selected stanza to English")
def set_language_to_english(modeladmin, request, queryset):
    queryset.update(language="en")


class StanzaAdmin(admin.ModelAdmin):
    inlines = [TextAnnotationInline, StanzaVariantInline]
    list_display = (
        "stanza_line_code_starts",
        "formatted_stanza_text",
        "language",
    )
    search_fields = (
        "stanza_text",
        "stanza_line_code_starts",
    )
    list_filter = ("language",)
    actions = [set_language_to_italian, set_language_to_english]

    class Media:
        css = {"all": ("css/text_annotations.css",)}
        js = ("js/text_annotations.js",)

    def formatted_stanza_text(self, obj):
        return format_html(obj.stanza_text)

    formatted_stanza_text.short_description = "Stanza Text"


class StanzaVariantAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if "stanza" in request.GET:
            initial["stanza"] = request.GET["stanza"]
        return initial


class StanzaTranslatedAdmin(admin.ModelAdmin):
    list_display = ("stanza", "stanza_text", "language")
    search_fields = ("stanza", "stanza_text")
    list_filter = ("language",)
    inlines = [TextAnnotationInline]

    class Media:
        css = {"all": ("css/text_annotations.css",)}
        js = ("js/text_annotations.js",)


class LineCodeAdmin(ImportExportModelAdmin):
    resource_class = LineCodeResource
    list_display = ("code", "get_toponyms", "get_folio")
    search_fields = ("code",)
    list_filter = ("associated_toponyms", "associated_folio__manuscript")
    filter_horizontal = ("associated_toponyms",)

    def get_toponyms(self, obj):
        return ", ".join([toponym.placename_id for toponym in obj.associated_toponyms.all()])

    def get_folio(self, obj):
        if obj.associated_folio:
            return f"{obj.associated_folio.manuscript.siglum}: {obj.associated_folio.folio_number}"
        return "-"

    get_toponyms.short_description = "Associated Toponyms (IDs)"
    get_folio.short_description = "Associated Folio"


admin.site.register(LineCode, LineCodeAdmin)

admin.site.register(Library, LibraryAdmin)
admin.site.register(Folio, FolioAdmin)
admin.site.register(SingleManuscript, SingleManuscriptAdmin)
admin.site.register(Stanza, StanzaAdmin)
admin.site.register(StanzaTranslated, StanzaTranslatedAdmin)
admin.site.register(TextAnnotation)

admin.site.site_header = "La Sfera Admin"
admin.site.site_title = "La Sfera Admin Portal"
admin.site.index_title = "Welcome to the La Sfera Manuscript Portal"
