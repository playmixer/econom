from rest_framework import serializers
from .models import Section, Wallet, CostCategory, IncomeCategory, Cost, Income
from django.contrib.auth import get_user_model
User = get_user_model()


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
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = CostCategory

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class IncomeCategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = IncomeCategory

    def create(self, validated_date):
        return IncomeCategory.objects.create(**validated_date)


class IncomeCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = IncomeCategory

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class CostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)
    wallet = serializers.IntegerField(source='wallet.id', required=False)
    category = serializers.IntegerField(source='category.id', required=False)
    cash = serializers.FloatField()

    class Meta:
        model = Cost

    def create(self, validated_date):
        return Cost.objects.create(**validated_date)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.cash = validated_data.get('cash', instance.cash)
        # instance.wallet = validated_data.get('wallet.id', instance.wallet)
        # instance.category = validated_data.get('category.id', instance.category)
        instance.save()
        return instance


class IncomeListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100)
    wallet = serializers.IntegerField(source='wallet.id', required=False)
    category = serializers.IntegerField(source='category.id', required=False)
    cash = serializers.FloatField()

    class Meta:
        model = Income

    def create(self, validated_date):
        return Income.objects.create(**validated_date)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.cash = validated_data.get('cash', instance.cash)
        # instance.wallet = validated_data.get('wallet.id', instance.wallet)
        # instance.category = validated_data.get('category.id', instance.category)
        instance.save()
        return instance
