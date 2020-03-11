from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Section, Wallet, CostCategory, IncomeCategory, Cost, Income
from .serializers import (
    SectionSerializer,
    WalletSerializer,
    WalletListSerializer,
    CostCategoryListSerializer,
    IncomeCategoryListSerializer,
    CostCategorySerializer,
    IncomeCategorySerializer,
    CostListSerializer,
    IncomeListSerializer,
)
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from apps.econom.utilits import transfer_cash


def get_section(id, user):
    try:
        return Section.objects.get(pk=id, user=user)
    except ObjectDoesNotExist:
        return None


def get_wallet(id_section, user, pk):
    section = get_section(id_section, user)
    if section is None:
        return None
    try:
        return Wallet.objects.get(section=section, pk=pk)
    except (ObjectDoesNotExist, AttributeError):
        return None


class SectionListView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        sections = Section.objects.filter(user=request.user)
        serializer = SectionSerializer(sections, many=True)
        return Response({'sections': serializer.data})

    def post(self, request, format=None):
        section = request.data.get('section')
        serializer = SectionSerializer(data=section)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response({"section": serializer.data})
        except IntegrityError:
            return Response({"error": f"Section '{section['title']}' exist"}, 400)


class SectionView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        section = get_section(pk, request.user)
        if section is None:
            return Response({"error": "Section not found"}, 400)
        serializer = SectionSerializer(section)
        return Response({"section": serializer.data})

    def put(self, request, pk):
        data = request.data.get('section')
        section = get_section(pk, request.user)
        if not section:
            return Response({"error": "Section not found"}, 400)
        serializer = SectionSerializer(section, data=data)
        if serializer.is_valid(raise_exception=True):
            section_saved = serializer.save()
            return Response(section_saved)
        return Response({"error": "Is not valid"}, 400)

    def delete(self, request, pk):
        section = get_section(pk, request.user)
        if not section:
            return Response({"error": "Section not found"}, 400)
        section.delete()
        return Response({})


class WalletListView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        wallets = Wallet.objects.filter(section=id_section)
        serializer = WalletListSerializer(wallets, many=True)
        return Response({"wallets": serializer.data})

    def post(self, request, id_section):
        wallet = request.data.get('wallet')
        section = get_section(id_section, request.user)
        if section is None:
            return Response({"error": "Section not found"}, 400)
        serializer = WalletSerializer(data=wallet)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(section=section)
                return Response({"wallet": serializer.data})
        except IntegrityError:
            return Response({"error": f"Wallet '{wallet['title']}' exist"}, 400)


class WalletView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section, pk):
        wallet = get_wallet(id_section, request.user, pk)
        if wallet is None:
            return Response({"error": "Wallet not found"}, 400)
        serializer = WalletSerializer(wallet)
        return Response({"wallet": serializer.data})

    def put(self, request, id_section, pk):
        data = request.data.get("wallet")
        wallet = get_wallet(id_section, request.user, pk)
        if wallet is None:
            return Response({"error": "Wallet not found"}, 400)
        serializer = WalletSerializer(wallet, data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                wallet_saved = serializer.save()
                return Response(wallet_saved)
        except IntegrityError:
            return Response({"error": f"Wallet '{serializer.data['title']}' is exist"}, 400)

    def delete(self, request, id_section, pk):
        wallet = get_wallet(id_section, request.user, pk)
        if wallet is None:
            return Response({"error": "Wallet not found"}, 400)
        wallet.delete()
        return Response({})


class CostCategoryListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        section = get_section(id_section, request.user)
        if section is None:
            Response({"error": "Section not found"}, 400)

        categories = CostCategory.objects.filter(section=section).order_by('title')
        serializer = CostCategoryListSerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request, id_section):
        category = request.data.get('category')
        section = Section.objects.get(pk=id_section, user=request.user)
        serializer = CostCategoryListSerializer(data=category)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(section=section)
                return Response({"category": serializer.data})
        except IntegrityError:
            return Response({"error": f"Category '{serializer.data['title']}' is exist"}, 400)


class CostCategoryView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def _category_exist(self, section, pk):
        try:
            return CostCategory.objects.get(pk=pk, section=section)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found"}, 400)

    def get(self, request, id_section, pk):
        section = get_section(request.user, id_section)
        if not section:
            Response({"error": "Section not found"}, 400)

        if not self._category_exist(section, pk):
            category = CostCategory.objects.get(pk=pk, section=section)

        serializer = CostCategorySerializer(category)
        return Response({"category": serializer.data})

    def put(self, request, id_section, pk):
        data = request.data.get('category')
        try:
            section = Section.objects.get(pk=id_section)
        except ObjectDoesNotExist:
            return Response({"error": "Section not found"}, 400)

        category = self._category_exist(section, pk)

        serialize = CostCategorySerializer(category, data=data)
        if serialize.is_valid(raise_exception=True):
            category_saved = serialize.save()
        return Response(category_saved)

    def delete(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        category = CostCategory.objects.get(pk=pk, section=section)
        category.delete()
        return Response({})


class IncomeCategoryListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        section = Section.objects.get(pk=id_section, user=request.user)
        categories = IncomeCategory.objects.filter(section=section).order_by('title')
        serializer = IncomeCategoryListSerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request, id_section):
        category = request.data.get('category')
        section = Section.objects.get(pk=id_section, user=request.user)
        serializer = IncomeCategoryListSerializer(data=category)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(section=section)
                return Response({"category": serializer.data})
        except IntegrityError:
            return Response({"error": f"Category '{serializer.data['title']}' is exist"}, 400)


class IncomeCategoryView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def _category_exist(self, section, pk):
        try:
            return IncomeCategory.objects.get(pk=pk, section=section)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found"}, 400)

    def get(self, request, id_section, pk):
        section = get_section(request.user, id_section)
        if not section:
            Response({"error": "Section not found"}, 400)
        category = self._category_exist(section, pk)
        serializer = IncomeCategorySerializer(category)
        return Response({"category": serializer.data})

    def put(self, request, id_section, pk):
        data = request.data.get('category')
        try:
            section = Section.objects.get(pk=id_section)
        except ObjectDoesNotExist:
            return Response({"error": "Section not found"}, 400)

        try:
            category = IncomeCategory.objects.get(pk=pk, section=section)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found"}, 400)

        serialize = IncomeCategorySerializer(category, data=data)
        if serialize.is_valid(raise_exception=True):
            category_saved = serialize.save()
        return Response(category_saved)

    def delete(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        category = IncomeCategory.objects.get(pk=pk, section=section)
        category.delete()
        return Response({})


class CostListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        try:
            section = Section.objects.get(pk=id_section, user=request.user)
            costs = Cost.objects.filter(section=section)
            serializer = CostListSerializer(costs, many=True)
            return Response({"costs": serializer.data})
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)

    def post(self, request, id_section):
        section = Section.objects.get(pk=id_section, user=request.user)
        cost = request.data.get('cost')
        if cost is None:
            return Response({"error": "Not found cost"}, 400)

        category = None
        if cost.get('category'):
            category = CostCategory.objects.get(pk=cost['category'])
        wallet = Wallet.objects.get(pk=cost['wallet'])
        serializer = CostListSerializer(data=cost)
        try:
            if serializer.is_valid(raise_exception=True):
                wallet.cash -= cost['cash']
                wallet.save()
                serializer.save(section=section, wallet=wallet, category=category)
                return Response({"cost": serializer.data})
        except IntegrityError:
            return Response({"error": serializer.data}, 400)


class CostView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section, pk):
        try:
            section = Section.objects.get(pk=id_section, user=request.user)
            cost = Cost.objects.get(pk=pk, section=section)
            serializer = CostListSerializer(cost)
            return Response({"cost": serializer.data})
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)

    def put(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        data = request.data.get('cost')
        cost = Cost.objects.get(pk=pk, section=section)
        if data.get('category'):
            cost.category = CostCategory.objects.get(pk=data['category'])
        wallet_from = cost.wallet
        cash_from = cost.cash
        wallet_to = Wallet.objects.get(pk=data['wallet'])
        cost.wallet = wallet_to
        serializer = CostListSerializer(cost, data=data)
        if serializer.is_valid(raise_exception=True):
            transfer_cash(wallet_from, cash_from, wallet_to, data['cash'])
            cost_saved = serializer.save()
            return Response({cost_saved})

    def delete(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        cost = Cost.objects.get(pk=pk, section=section)
        wallet = cost.wallet
        wallet.cash += cost.cash
        wallet.save()
        cost.delete()
        return Response({})


class IncomeListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        try:
            section = Section.objects.get(pk=id_section, user=request.user)
            incomes = Income.objects.filter(section=section)
            serializer = IncomeListSerializer(incomes, many=True)
            return Response({"incomes": serializer.data})
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)

    def post(self, request, id_section):
        section = Section.objects.get(pk=id_section, user=request.user)
        income = request.data.get('income')
        if income is None:
            return Response({"error": "Not found"}, 400)
        category = None
        if income.get('category'):
            category = IncomeCategory.objects.get(pk=income['category'])
        wallet = Wallet.objects.get(pk=income['wallet'])
        serializer = IncomeListSerializer(data=income)
        try:
            if serializer.is_valid(raise_exception=True):
                wallet.cash += income['cash']
                wallet.save()
                serializer.save(section=section, wallet=wallet, category=category)
                return Response({"income": serializer.data})
        except IntegrityError:
            return Response({"error": serializer.data}, 400)


class IncomeView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        data = Income.objects.get(pk=pk, section=section)
        serializer = IncomeListSerializer(data)
        return Response({'income': serializer.data})

    def put(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        data = request.data.get('income')
        income = Income.objects.get(pk=pk, section=section)
        if data.get('category'):
            income.category = IncomeCategory.objects.get(pk=data['category'])
        wallet_from = income.wallet
        cash_from = income.cash
        wallet_to = Wallet.objects.get(pk=data['wallet'])
        income.wallet = wallet_to
        serializer = IncomeListSerializer(income, data=data)
        if serializer.is_valid(raise_exception=True):
            transfer_cash(wallet_from, cash_from, wallet_to, data['cash'])
            income_saved = serializer.save()
            return Response({income_saved})

    def delete(self, request, id_section, pk):
        section = Section.objects.get(pk=id_section, user=request.user)
        income = Income.objects.get(pk=pk, section=section)
        wallet = income.wallet
        wallet.cash -= income.cash
        wallet.save()
        income.delete()
        return Response({})




