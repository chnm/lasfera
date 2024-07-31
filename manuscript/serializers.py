from rest_framework import serializers

from manuscript.models import Location, SingleManuscript


class ToponymSerializer(serializers.ModelSerializer):
    detailed_toponym = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["id", "country", "latitude", "longitude", "detailed_toponym"]

    def get_detailed_toponym(self, obj):
        return {
            "id": obj.id,
            "country": obj.country,
            "latitude": obj.latitude,
            "longitude": obj.longitude,
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
