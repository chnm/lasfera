from rest_framework import serializers

from manuscript.models import Location, LocationAlias, SingleManuscript


class ToponymSerializer(serializers.ModelSerializer):
    aliases = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["id", "modern_country", "latitude", "longitude", "aliases"]

    def get_aliases(self, obj):
        aliases = (
            LocationAlias.objects.filter(location=obj)
            .values_list("placename_modern", flat=True)
            .distinct()
        )
        return {
            "id": obj.id,
            "placename_modern": list(aliases),
        }


class SingleManuscriptSerializer(serializers.ModelSerializer):
    manuscript = serializers.SerializerMethodField()

    class Meta:
        model = SingleManuscript
        fields = ["id", "siglum", "iiif_url", "photographs", "manuscript"]

    def get_manuscript(self, obj):
        photographs = (
            obj.photographs.url
            if obj.photographs and hasattr(obj.photographs, "url")
            else None
        )
        return {
            "id": obj.id,
            "siglum": obj.siglum,
            "iiif_url": obj.iiif_url,
            "photographs": photographs,
        }
