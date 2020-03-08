from rest_framework import serializers
from .models import Section, Wallet, CostCategory, IncomeCategory
from django.contrib.auth.models import User


class SectionSerializer(serializers.Serializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = Section

    def create(self, validated_data):
        return Section.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)

        instance.save()
        return instance


class WalletListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    section_name = serializers.CharField(source='section.title', read_only=True)
    title = serializers.CharField(max_length=100)
    cash = serializers.FloatField()

    class Meta:
        model = Wallet
        fields = '__all__'


class WalletSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    # section_name = serializers.CharField(source='section.title', read_only=True)
    title = serializers.CharField(max_length=100)
    cash = serializers.FloatField()

    class Meta:
        model = Wallet
        fields = '__all__'

    def create(self, validated_data):
        return Wallet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.cash = validated_data.get('cash', instance.cash)
        instance.save()
        return instance


class CostCategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = CostCategory

    def create(self, validated_date):
        return CostCategory.objects.create(**validated_date)


class CostCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)

    class Meta:
        model = CostCategory

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class IncomeCategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)

    class Meta:
        model = IncomeCategory
