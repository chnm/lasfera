from collections import defaultdict
from html import unescape

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from manuscript.models import Location, SingleManuscript, Stanza, StanzaTranslated
from manuscript.serializers import SingleManuscriptSerializer, ToponymSerializer


def process_stanzas(stanzas, is_translated=False):
    books = defaultdict(lambda: defaultdict(list))
    for stanza in stanzas:
        book_number = int(stanza.stanza_line_code_starts.split(".")[0])
        stanza_number = int(stanza.stanza_line_code_starts.split(".")[1])

        if is_translated:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_text)
        else:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_text)

        books[book_number][stanza_number].append(stanza)

    return {k: dict(v) for k, v in books.items()}


def index(request: HttpRequest):
    return render(request, "index.html")


def about(request: HttpRequest):
    return render(request, "about.html")


def stanzas(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")
    translated_stanzas = StanzaTranslated.objects.all().order_by(
        "stanza_line_code_starts"
    )
    manuscripts = SingleManuscript.objects.all()
    default_manuscript = SingleManuscript.objects.get(siglum="TEST")

    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas)

    books = {k: dict(v) for k, v in books.items()}
    translated_books = {k: dict(v) for k, v in translated_books.items()}

    return render(
        request,
        "stanzas.html",
        {
            "stanzas": stanzas,
            "translated": translated_stanzas,
            "books": books,
            "translated_books": translated_books,
            "manuscripts": manuscripts,
            "default_manuscript": default_manuscript,
        },
    )


def manuscripts(request: HttpRequest):
    manuscript_objs = SingleManuscript.objects.all()
    return render(request, "manuscripts.html", {"manuscripts": manuscript_objs})


def manuscript(request: HttpRequest, siglum: str):
    get_manuscript = get_object_or_404(SingleManuscript, siglum=siglum)
    folios = get_manuscript.folio_set.prefetch_related("locations_mentioned").all()
    return render(
        request,
        "manuscript_single.html",
        {
            "manuscript": get_manuscript,
            "folios": folios,
            "iiif_manifest": get_manuscript.iiif_url,
        },
    )


def toponyms(request: HttpRequest):
    toponym_objs = Location.objects.all()
    return render(request, "gazetteer/gazetteer_index.html", {"toponyms": toponym_objs})


def toponym(request: HttpRequest, toponym_param: int):
    print("toponym_param", toponym_param)
    filtered_toponym = get_object_or_404(Location, pk=toponym_param)
    filtered_manuscripts = SingleManuscript.objects.filter(
        folio__locations_mentioned=toponym_param
    ).distinct()
    filtered_folios = filtered_toponym.folio_set.all()
    processed_aliases = []

    for alias in filtered_toponym.locationalias_set.all():
        placename_alias = (
            [name.strip() for name in alias.placename_alias.split(",")]
            if alias.placename_alias
            else []
        )
        placename_modern = (
            [name.strip() for name in alias.placename_modern.split(",")]
            if alias.placename_modern
            else []
        )
        placename_standardized = (
            [name.strip() for name in alias.placename_standardized.split(",")]
            if alias.placename_standardized
            else []
        )
        placename_from_mss = (
            [name.strip() for name in alias.placename_from_mss.split(",")]
            if alias.placename_from_mss
            else []
        )

        processed_aliases.append(
            {
                "placename_alias": placename_alias,
                "placename_modern": placename_modern,
                "placename_standardized": placename_standardized,
                "placename_from_mss": placename_from_mss,
            }
        )

    # Get associated iiif_url fields from SingleManuscript
    for manuscript in filtered_manuscripts:
        manuscript.iiif_url = manuscript.iiif_url

    return render(
        request,
        "gazetteer/gazetteer_single.html",
        {
            "toponym": filtered_toponym,
            "manuscripts": filtered_manuscripts,
            "aliases": processed_aliases,
            "folios": filtered_folios,
            "iiif_manifest": filtered_manuscripts[0].iiif_url,
        },
    )


def search_toponyms(request):
    query = request.GET.get("q", "")
    if query:
        toponym_results = Location.objects.filter(country__icontains=query)
    else:
        toponym_results = Location.objects.all()
    return render(
        request, "gazetteer/gazetteer_results.html", {"toponyms": toponym_results}
    )


class ToponymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ToponymSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset based on the 'q' query parameter
        and returns all objects if no specific filter is applied.
        """
        queryset = Location.objects.all()
        query = self.request.query_params.get("q", None)
        if query is not None:
            queryset = queryset.filter(country__icontains=query)
        return queryset


class SingleManuscriptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SingleManuscriptSerializer
    lookup_field = "siglum"

    def get_queryset(self):
        """
        Optionally filters the queryset based on the 'q' query parameter
        and returns all objects if no specific filter is applied.
        """
        queryset = SingleManuscript.objects.all()
        query = self.request.query_params.get("q", None)
        if query is not None:
            queryset = queryset.filter(siglum__icontains=query)
        return queryset
