import logging
import re

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from prose.fields import RichTextField

logger = logging.getLogger(__name__)


def validate_line_number_code(value):
    pattern = r"^\d{2}\.\d{2}\.\d{2}(-\d{2}\.\d{2}\.\d{2})?$"
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid number format. Expected format: "01.01.04" or "01.01.04-01.01.16"'
        )


def validate_line_number_variant_code(value):
    # expected: 01.01.04a or 04.05.01b etc.
    pattern = r"^\d{2}\.\d{2}\.\d{2}[a-z]$"
    if not re.match(pattern, value):
        raise ValidationError('Invalid number format. Expected format: "01.01.04a"')


class LineCode(models.Model):
    code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Input the text by book, stanza, and line number. For example: 01.01.01 refers to book 1, stanza 1, line 1.",
        validators=[validate_line_number_code],
    )
    associated_iiif_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the IIIF manifest for the manuscript. If there isn't one, leave blank.",
        verbose_name="Associated IIIF URL",
    )
    associated_toponym = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    associated_folio = models.ForeignKey(
        "Folio",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.code)


class Library(models.Model):
    """Library or collection that holds a manuscript"""

    city = models.CharField(max_length=255, blank=True, null=True)
    library = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Libraries"
        unique_together = ["city", "library"]
        ordering = ["city", "library"]

    def __str__(self) -> str:
        city = self.city if self.city is not None else "No city name provided"
        library = self.library if self.library is not None else ""
        return city + " - " + library

    def natural_key(self):
        return (self.library, self.city)


class EditorialStatus(models.Model):
    """The editorial status of a manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    # siglum = models.CharField(max_length=255, blank=True, null=True, unique=True)
    editorial_priority = models.IntegerField(blank=True, null=True)
    collated = models.CharField(blank=True, null=True, max_length=510)
    access = models.IntegerField(blank=True, null=True)
    spatial_priority = models.CharField(max_length=6, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    map_group = models.CharField(max_length=255, blank=True, null=True)
    decorative_group = models.CharField(max_length=255, blank=True, null=True)
    iiif_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the IIIF manifest for the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )

    class Meta:
        verbose_name = "Editorial Status"
        verbose_name_plural = "Editorial Status"

    def __str__(self) -> str:
        if self.editorial_priority is not None:
            return "Editorial Priority: " + str(self.editorial_priority)
        return "Editorial Status"


class Reference(models.Model):
    """References within the manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    bert = models.CharField(max_length=6, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        if self.reference is not None:
            return self.reference
        return "Reference"


class Codex(models.Model):
    """Information and details about the manuscript"""

    id = models.AutoField(primary_key=True)
    support = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True, help_text="in cm")
    date = models.CharField(max_length=255, blank=True, null=True)
    folia = models.CharField(max_length=255, blank=True, null=True)
    lines_per_page = models.CharField(max_length=255, blank=True, null=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Codex"

    def __str__(self) -> str:
        if self.id is not None:
            return str(self.id)
        return str(self.id)


class TextDecoration(models.Model):
    """Details and information about the text of the manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.CharField(blank=True, null=True, max_length=510)
    maps = models.CharField(blank=True, null=True, max_length=510)
    illumination = models.CharField(blank=True, null=True, max_length=510)
    white_vine_work = models.CharField(blank=True, null=True, max_length=510)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        if self.text_script is not None:
            return self.text_script
        else:
            return "Text Decoration"


class Detail(models.Model):
    """Details about the manuscript including author, scribe, headings, etc."""

    STANZA_RUBRIC_CHOICES = (
        ("sh", "Stanza Headings"),
        ("mr", "Marginal Rubrics"),
        ("ne", "Neither"),
        ("uk", "Unknown"),
    )

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    author_attribution = models.CharField(max_length=510, blank=True, null=True)
    scribe_attribution = models.CharField(max_length=510, blank=True, null=True)
    book_headings = RichTextField(blank=True, null=True)
    book_initials = RichTextField(blank=True, null=True)
    stanza_headings_marginal_rubrics = models.CharField(
        max_length=2, choices=STANZA_RUBRIC_CHOICES, blank=True, null=True
    )
    stanza_headings_marginal_rubrics_notes = RichTextField(
        max_length=510, blank=True, null=True
    )
    stanza_initials = RichTextField(max_length=510, blank=True, null=True)
    stanzas_separated = models.CharField(blank=True, null=True, max_length=510)
    stanzas_ed = models.CharField(blank=True, null=True, max_length=510)
    filigree = models.CharField(
        max_length=510,
        blank=True,
        null=True,
        verbose_name="Flourished/Filigree Initials",
    )
    standard_water = models.CharField(blank=True, null=True, max_length=510)
    abbreviations = RichTextField(max_length=510, blank=True, null=True)
    catchwords = RichTextField(max_length=510, blank=True, null=True)
    mabel_label = models.CharField(max_length=510, blank=True, null=True)
    map_labels = RichTextField(max_length=510, blank=True, null=True)
    distance_lines = models.CharField(blank=True, null=True, max_length=510)
    distance_numbers = models.CharField(max_length=510, blank=True, null=True)
    coat_of_arms = models.CharField(max_length=510, blank=True, null=True)

    is_sea_red = models.CharField(
        blank=True,
        null=True,
        verbose_name="Is the Red Sea colored red?",
        max_length=510,
    )
    laiazzo = models.CharField(blank=True, null=True, max_length=510)
    tabriz = models.CharField(blank=True, null=True, max_length=510)
    rhodes_status = models.CharField(max_length=510, blank=True, null=True)
    gion_in_egypt = models.CharField(max_length=510, blank=True, null=True)
    diagram_sun = models.CharField(max_length=510, blank=True, null=True)

    def __str__(self) -> str:
        if self.id is not None:
            return str(self.id)
        else:
            return "Detail"


class ViewerNote(models.Model):
    """Notes on the manuscript from a particular user"""

    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="viewer",
        help_text="The user who viewed the manuscript.",
    )

    notes = models.TextField(blank=True, null=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self) -> str:
        if self.viewer is not None:
            return self.viewer
        return "Viewer Note"


class StanzaVariant(models.Model):
    """Notes about variants in a stanza"""

    AVAIL_LANGUAGE = (
        ("en", "English"),
        ("it", "Italian"),
    )

    # TODO: Ability to have variation in lines
    id = models.AutoField(primary_key=True)
    stanza_variation = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Significant Variations",
        help_text="The variation in the stanza.",
    )
    stanza_variation_line_code_starts = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_variant_code],
        max_length=20,
        help_text="Stanza variant line code in the form of '01.01.01a'.",
        verbose_name="Variant line code",
    )
    stanza = models.ForeignKey(
        "Stanza",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        editable=False,
    )

    def provide_snippet_of_stanza(self):
        return self.stanza.stanza_variation[:100]

    def save(self, *args, **kwargs):
        # we trim the letter code off the stanza_variation_line_code_starts
        # so we can look for the FK to the Stanza
        try:
            stanza_line_code_starts = self.stanza_variation_line_code_starts[:-1]
        except TypeError:
            stanza_line_code_starts = None

        try:
            self.stanza = Stanza.objects.get(
                stanza_line_code_starts=stanza_line_code_starts
            )
        except ObjectDoesNotExist:
            pass

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            "Stanza "
            + self.stanza_variation_line_code_starts
            + " associated with "
            + self.stanza.stanza_line_code_starts
            + " ("
            + self.stanza.related_manuscript.siglum
            + ")"
        )


class Stanza(models.Model):
    """A stanza from the manuscript."""

    STANZA_LANGUAGE = (
        ("en", "English"),
        ("it", "Italian"),
        ("la", "Latin"),
        ("fr", "French"),
    )

    id = models.AutoField(primary_key=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text="Required. The manuscript to which the stanza belongs.",
    )
    related_folio = models.ForeignKey(
        "Folio",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Optional. The folio to which the stanza belongs.",
    )
    stanza_line_code_starts = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the folio begins. Input the text by book, stanza, and line number. For example: 01.01.01 refers to book 1, stanza 1, line 1.",
    )
    stanza_line_code_ends = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the folio ends. Input the text by book, stanza, and line number. For example: 01.01.07 refers to book 1, stanza 1, line 7.",
    )
    stanza_text = RichTextField(blank=True, null=True)
    stanza_notes = RichTextField(blank=True, null=True)
    language = models.CharField(
        max_length=2, choices=STANZA_LANGUAGE, blank=True, null=True
    )

    def __str__(self) -> str:
        if self.stanza_line_code_starts is not None:
            return self.stanza_line_code_starts
        elif self.stanza_line_code_ends is not None:
            return self.stanza_line_code_starts + " - " + self.stanza_line_code_ends
        elif self.stanza_line_variation is not None:
            return (
                self.stanza_line_code_starts
                + " - "
                + self.stanza_line_code_ends
                + " - "
                + self.stanza_line_variation
            )
        else:
            return ""

    def get_book(self):
        return int(self.stanza_line_code.split(".")[0])

    def get_stanza(self):
        return int(self.stanza_line_code.split(".")[1])

    def get_line(self):
        return int(
            self.your_field.split(".")[2].split("-")[0]
        )  # Handle the case of a range

    def derive_folio_location(self):
        # We derive the folio based on the line code.
        # if self.stanza_line_code_starts is not None:
        #     line_code = self.stanza_line_code_starts
        # elif self.stanza_line_code_ends is not None:
        #     line_code = self.stanza_line_code_ends
        # else:
        #     return None
        #
        # book, stanza, line = line_code.split(".")
        # return Folio.objects.filter(
        #     manuscript=self.related_folio.manuscript, folio_number=book
        # ).first()
        start_book, start_stanza, start_line = map(int, start_line.split("."))
        end_book, end_stanza, end_line = map(int, end_line.split("."))

        for line in range(start_line, end_line + 1):
            line_code = f"{start_book:02d}.{start_stanza:02d}.{line:02d}"
            existing_stanzas = Stanza.objects.filter(
                stanza_line_code_starts__startswith=line_code
            )
            variant_code = line_code + chr(ord("a") + existing_stanza.count())

            try:
                self.stanza = Stanza.objects.get(stanza_line_code_starts=variant_code)
            except ObjectDoesNotExist:
                pass

            folio = Folio.objects.filter(
                manuscript=self.related_folio.manuscript, folio_number=start_book
            ).first()

            Stanza.objects.create(
                related_manuscript=self.related_folio.manuscript,
                related_folio=folio,
                stanza_line_code_starts=variant_code,
                stanza_line_code_end=variant_code,
                stanza_text=self.stanza_text,
                stanza_notes=self.stanza_notes,
                language=self.language,
            )

    class Meta:
        ordering = ["id"]


class StanzaTranslated(models.Model):
    """This model holds the English version of the stanzas."""

    id = models.AutoField(primary_key=True)
    stanza = models.ForeignKey(
        "Stanza",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text="The stanza to which the translation belongs.",
    )
    stanza_line_code_starts = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the stanza begins. Input the text by book, stanza, and line number. For example: 01.01.01 refers to book 1, stanza 1, line 1.",
    )
    stanza_line_code_ends = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the stanza ends. Input the text by book, stanza, and line number. For example: 01.01.07 refers to book 1, stanza 1, line 7.",
    )
    stanza_text = RichTextField(blank=True, null=True)
    language = models.CharField(
        max_length=2, choices=Stanza.STANZA_LANGUAGE, blank=True, null=True
    )

    def __str__(self) -> str:
        return str(self.stanza_text[:100])

    class Meta:
        verbose_name = "Stanza translation"
        verbose_name_plural = "Stanza translations"


class Folio(models.Model):
    """This provides a way to collect several stanzas onto a single page, and associate them with a single manuscript."""

    FOLIO_MAP_CHOICES = (
        ("yes", "Yes"),
        ("yes_toponyms", "Yes with toponyms"),
        ("yes_no_toponyms", "Yes without toponyms"),
        ("no", "No"),
    )

    id = models.AutoField(primary_key=True)
    folio_number = models.CharField(blank=True, null=True, max_length=510)
    folio_notes = RichTextField(blank=True, null=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    image = models.ImageField(
        null=True,
        blank=True,
        help_text="The image of the page from the manuscript.",
    )
    iiif_url = models.URLField(
        blank=True,
        null=True,
        help_text="Provide a IIIF manifest to a page in the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )
    folio_includes_map = models.CharField(
        blank=True,
        null=True,
        choices=FOLIO_MAP_CHOICES,
        verbose_name="Does the folio include a map?",
        max_length=510,
    )
    locations_mentioned = models.ManyToManyField(
        "Location",
        blank=True,
        help_text="Toponyms associated with the folio.",
        verbose_name="Associated toponyms",
    )

    def __str__(self) -> str:
        if self.folio_number is not None:
            return f"Folio {self.folio_number}, from manuscript {self.manuscript}"
        return f"Folio has no folio number, but is associated with manuscript {self.manuscript}"

    class Meta:
        ordering = ["folio_number"]


class SingleManuscript(models.Model):
    """A representation of a single manuscript"""

    id = models.AutoField(primary_key=True)
    item_id = models.IntegerField(blank=False, null=False, unique=True)
    siglum = models.CharField(
        max_length=20, blank=True, null=True, unique=True, db_index=True
    )
    shelfmark = models.CharField(max_length=255, blank=True, null=True)
    library = models.ForeignKey(
        Library, on_delete=models.PROTECT, blank=True, null=True
    )
    iiif_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the IIIF manifest for the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )
    gazetteer_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to an external gazetteer for the manuscript. If there isn't one, leave blank.",
        verbose_name="Gazetteer URL",
    )
    purl_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL to the permanent URL for the manuscript. If there isn't one, leave blank.",
        verbose_name="Permanent URL",
    )
    digitized_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="The URL to the digitized manuscript. If there isn't one, leave blank.",
        verbose_name="Digitized URL",
    )
    photographs = models.FileField(
        blank=True,
        null=True,
        help_text="Upload photographs of the manuscript.",
    )

    provenance = RichTextField(blank=True, null=True)
    manuscript_lost = models.BooleanField(blank=True, null=True, default=False)
    manuscript_destroyed = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        verbose_name = "Manuscript"
        verbose_name_plural = "Manuscripts"
        ordering = ["siglum"]

    def __str__(self) -> str:
        if self.siglum:
            return self.siglum
        elif self.shelfmark:
            return self.shelfmark
        else:
            return "Manuscript"

    def has_pdf_or_images(self):
        if self.photographs:
            return self.photographs.name.endswith((".pdf", ".jpg", ".jpeg", ".png"))
        return False


class AuthorityFile(models.Model):
    """Include authority files for various aspects of a manuscript"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The name of the authority file",
    )
    authority_file_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL to the authority file for the manuscript.",
        verbose_name="Authority File URL",
    )
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.authority_file_url}"

    class Meta:
        verbose_name = "Authority File"
        verbose_name_plural = "Authority Files"


class Location(models.Model):
    """Handle the location information and toponyms within a manuscript"""

    CODE_CHOICE = (("mp", "Map"), ("pm", "Poem"))

    id = models.AutoField(primary_key=True)
    toponym_type = models.CharField(
        blank=True,
        null=True,
        choices=CODE_CHOICE,
        max_length=2,
        help_text="The type will be automatically set based off the placename ID.",
    )
    placename_id = models.CharField(
        blank=True, null=True, verbose_name="Placename ID", max_length=510
    )
    country = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Modern location"
    )
    description = RichTextField(blank=True, null=True)
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Latitude in decimal degrees. If left blank, the system will attempt to geocode the location from the modern placename.",
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Longitude in decimal degrees. If left blank, the system will attempt to geocode the location from the modern placename.",
    )
    authority_file = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the authority file for the location. If there isn't one, leave blank.",
    )

    class Meta:
        verbose_name = "Toponym"
        verbose_name_plural = "Toponyms"
        ordering = ["country"]
        unique_together = ["country"]

    def __str__(self) -> str:
        return (
            self.country if self.country is not None else "Missing modern country name"
        )

    def geocode(self):
        try:
            from geopy.geocoders import Nominatim

            geolocator = Nominatim(user_agent="lasfera_manuscript")

            if self.country:
                # Define the bounding box for Europe and Africa
                europe_africa_bbox = {
                    "viewbox": [
                        (
                            -31.266001,
                            -34.83333,
                        ),  # Southwest corner (longitude, latitude)
                        (63.33333, 71.20868),  # Northeast corner (longitude, latitude)
                    ],
                    "bounded": True,
                }

                location = geolocator.geocode(self.country, **europe_africa_bbox)
                if location is not None:
                    self.latitude = str(location.latitude)
                    self.longitude = str(location.longitude)
                    self.save()
        except Exception as e:
            logger.warning("Warning in geocoding a toponym: %s %s", str(e), str(self))

    def save(self, *args, **kwargs):
        # We attempt to automatically set the toponym type based on the code_id
        if self.placename_id:
            prefix = self.placename_id[0].upper()
            if prefix == "M":
                self.toponym_type = "mp"
            elif prefix == "P":
                self.toponym_type = "pm"
        super(Location, self).save(*args, **kwargs)


class LocationAlias(models.Model):
    """The alias of a location"""

    id = models.AutoField(primary_key=True)
    placename_from_mss = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Transcribed placename",
        help_text="The placename as it appears in the manuscript.",
    )
    placename_standardized = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Standardized placename",
        help_text="The standardized name of the placename.",
    )
    placename_modern = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Modern placename",
        help_text="The modern name of the placename.",
    )
    placename_alias = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Additional aliases",
        help_text="Additional aliases for the placename.",
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Location Alias"
        verbose_name_plural = "Location Aliases"
        ordering = ["placename_standardized"]
        unique_together = ["placename_standardized"]

    def __str__(self) -> str:
        return f"{self.placename_from_mss} / {self.placename_standardized} / {self.placename_modern} / {self.placename_alias}"
