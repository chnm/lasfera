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


class LineCodeInline(admin.TabularInline):
    model = LineCode
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
        "item_id",
    )
    search_fields = ("siglum",)
    resource_class = SingleManuscriptResource

    class Media:
        js = ("js/text_annotator.js",)
        css = {"all": ("css/text_annotator.css",)}


class FolioAdmin(admin.ModelAdmin):
    inlines = [
        StanzaInline,
    ]
    list_filter = ("manuscript",)
    list_display = (
        "folio_number",
        "manuscript",
    )
    search_fields = (
        "folio_number",
        "manuscript__siglum",
    )

    def add_link_to_edit_stanzas(self, obj):
        url = reverse("admin:manuscript_stanza_add") + "?folio=" + str(obj.id)
        return format_html('<a href="{}">Add Stanza</a>', url)

    def manuscript(self, obj):
        url = reverse(
            "admin:manuscript_singlemanuscript_change", args=[obj.singlemanuscript.id]
        )
        return format_html('<a href="{}">{}</a>', url, obj.singlemanuscript.siglum)


class ReferenceAdmin(ImportExportModelAdmin):
    list_display = ("reference", "bert")
    resource_class = ReferenceResource


class LibraryAdmin(admin.ModelAdmin):
    list_display = ("library", "city", "id")
    list_filter = ("city",)


class EditorialStatusAdmin(admin.ModelAdmin):
    list_display = ("editorial_priority", "spatial_priority")
    resource_class = EditorialStatusResource


class CodexAdmin(admin.ModelAdmin):
    list_display = ("id", "support", "height", "folia", "date")


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    list_display = (
        "placename_id",
        "get_placename_modern",
        "get_mss_placename",
        "toponym_type",
        "place_type",
        "get_related_folios",
        "id",
    )
    search_fields = ("placename_id", "description", "modern_country")
    inlines = [LocationAliasInline, LineCodeInline]

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
        "display_folio",
        "formatted_stanza_text",
        "display_stanza_variants",
        "language",
    )
    search_fields = (
        "stanza_text",
        "stanza_line_code_starts",
    )
    actions = [set_language_to_italian, set_language_to_english]

    class Media:
        css = {"all": ("css/text_annotations.css",)}
        js = ("js/text_annotations.js",)

    def display_folio(self, obj):
        if obj.related_folio:
            return f"Folio {obj.related_folio.folio_number}"
        return "-"

    display_folio.short_description = "Folio"

    def formatted_stanza_text(self, obj):
        return format_html(obj.stanza_text)

    formatted_stanza_text.short_description = "Stanza Text"

    # List any stanza variants associated with a stanza
    def display_stanza_variants(self, obj):
        variants = ["- {}".format(variant) for variant in obj.stanzavariant_set.all()]
        return format_html("<br>".join(variants))

    display_stanza_variants.short_description = "Stanza Variants"


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


admin.site.register(Library, LibraryAdmin)
admin.site.register(EditorialStatus, EditorialStatusAdmin)
admin.site.register(Folio, FolioAdmin)
admin.site.register(SingleManuscript, SingleManuscriptAdmin)
admin.site.register(Stanza, StanzaAdmin)
admin.site.register(StanzaVariant, StanzaVariantAdmin)
admin.site.register(StanzaTranslated, StanzaTranslatedAdmin)
admin.site.register(LineCode)
admin.site.register(TextAnnotation)

admin.site.site_header = "La Sfera Admin"
admin.site.site_title = "La Sfera Admin Portal"
admin.site.index_title = "Welcome to the La Sfera Manuscript Portal"
