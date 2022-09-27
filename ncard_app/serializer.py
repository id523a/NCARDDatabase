from rest_framework import serializers
from ncard_app import models


class RecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    recipients = RecipientsSerializer(many=True, read_only=True)
    award_type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = models.Award
        fields = '__all__'

    def get_award_type(self, obj):
        return obj.get_award_type_display()

    def get_status(self, obj):
        return obj.get_status_display()
