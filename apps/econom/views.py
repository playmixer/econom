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
)
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from apps.econom.utilits import change_cost_wallet

"""
post
{
    "section": {
        "title": "Section"
    }
}
         
put
{
    "section": {
        "id": 1,
        "title": "Section"
    }
}

"""


def section_exist(user, id):
    try:
        Section.objects.get(pk=id, user=user)
        return True
    except ObjectDoesNotExist:
        return False


class SectionListView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, fromat=None):
        sections = Section.objects.filter(user=request.user)
        serializer = SectionSerializer(sections, many=True)
        return Response({'sections': serializer.data})

    def post(self, request, format=None):
        section = request.data.get('section')
        serializer = SectionSerializer(data=section)
        try:
            if serializer.is_valid(raise_exception=True):
                section_saved = serializer.save(user=request.user)
                return Response({"section": serializer.data})
        except IntegrityError:
            return Response({"error": f"Section '{section['title']}' exist"}, 400)


class SectionView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            section = Section.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)

        serializer = SectionSerializer(section)
        return Response({"section": serializer.data})

    def put(self, request, pk):
        data = request.data.get('section')
        try:
            section = Section.objects.get(pk=pk, user=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)
        serializer = SectionSerializer(section, data=data)
        if serializer.is_valid(raise_exception=True):
            section_saved = serializer.save()
            return Response(section_saved)
        return Response({"error": "Is not valid"}, 400)

    def delete(self, request, pk):
        try:
            section = Section.objects.filter(pk=pk, user=request.user)
            section.delete()
            return Response({})
        except (AttributeError, ObjectDoesNotExist):
            return Response({"error": "Not found"}, 400)


"""

wallet post
{"wallet":{"title":"wallet1", "cash":0}}
"""


class WalletListView(APIView, TokenAuthentication):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        wallets = Wallet.objects.filter(section=id_section)
        serializer = WalletListSerializer(wallets, many=True)
        return Response({"wallets": serializer.data})

    def post(self, request, id_section):
        wallet = request.data.get('wallet')
        section = Section.objects.get(pk=id_section, user=request.user)
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

    def _exist(self, request, id_section=None, id_wallet=None):
        if id_section:
            try:
                section = Section.objects.get(pk=id_section, user=request.user)
            except ObjectDoesNotExist:
                return "Section not found"

        if id_wallet:
            try:
                Wallet.objects.get(pk=id_wallet, section=section)
            except ObjectDoesNotExist:
                return "Wallet not found"

        return False

    def get(self, request, id_section, pk):
        is_not_exist = self._exist(request, id_section=id_section, id_wallet=pk)
        if is_not_exist:
            return Response({"error": is_not_exist}, 400)

        section = Section.objects.get(pk=id_section, user=request.user)
        wallet = Wallet.objects.get(pk=pk, section=section)

        serializer = WalletSerializer(wallet)
        return Response({"wallet": serializer.data})

    def put(self, request, id_section, pk):
        is_not_exist = self._exist(request, id_section=id_section, id_wallet=pk)
        if is_not_exist:
            return Response({"error": is_not_exist}, 400)
        data = request.data.get("wallet")
        section = Section.objects.get(pk=id_section, user=request.user)
        wallet = Wallet.objects.get(section=section, pk=pk)
        serializer = WalletSerializer(wallet, data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                wallet_saved = serializer.save()
                return Response(wallet_saved)
            return Response({"error": "Is not valid"}, 400)
        except IntegrityError:
            return Response({"error": f"Wallet '{serializer.data['title']}' is exist"}, 400)

    def delete(self, request, id_section, pk):
        is_not_exist = self._exist(request, id_section=id_section, id_wallet=pk)
        if is_not_exist:
            return Response({"error": is_not_exist}, 400)

        section = Section.objects.get(pk=id_section, user=request.user)
        wallet = Wallet.objects.get(pk=pk, section=section)
        try:
            wallet.delete()
            return Response({})
        except (AttributeError, ObjectDoesNotExist):
            return Response({"error": "Not found"}, 400)


class CostCategoryListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_section):
        section = Section.objects.get(pk=id_section, user=request.user)
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
            CostCategory.objects.get(pk=pk, section=section)
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, id_section, pk):
        if not section_exist(request.user, id_section):
            return Response({"error": "Section not found"}, 400)

        section = Section.objects.get(pk=id_section, user=request.user)

        if not self._category_exist(section, pk):
            return Response({"error": "Category not found"}, 400)

        category = CostCategory.objects.get(pk=pk, section=section)
        serializer = CostCategorySerializer(category)
        return Response({"category": serializer.data})

    def put(self, request, id_section, pk):
        data = request.data.get('category')
        try:
            section = Section.objects.get(pk=id_section)
        except ObjectDoesNotExist:
            return Response({"error": "Section not found"}, 400)

        try:
            category = CostCategory.objects.get(pk=pk, section=section)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found"}, 400)

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
            IncomeCategory.objects.get(pk=pk, section=section)
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, id_section, pk):
        if not section_exist(request.user, id_section):
            return Response({"error": "Section not found"}, 400)

        section = Section.objects.get(pk=id_section, user=request.user)

        if not self._category_exist(section, pk):
            return Response({"error": "Category not found"}, 400)

        category = IncomeCategory.objects.get(pk=pk, section=section)
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
            return Response({"error": "Not found cost"})

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
            change_cost_wallet(wallet_from, cash_from, wallet_to, data['cash'])
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

