from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Section, Wallet, CostCategory, IncomeCategory
from .serializers import SectionSerializer, WalletSerializer, WalletListSerializer, CostCategoryListSerializer, \
    IncomeCategoryListSerializer, CostCategorySerializer
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

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

    def get(self, request, pk, fromat=None):
        try:
            section = Section.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, 400)

        serializer = SectionSerializer(section)
        return Response({"section": serializer.data})

    def put(self, request, pk, format=None):
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

    def delete(self, request, pk, format=None):
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
        categories = CostCategory.objects.filter(Q(section=None) | Q(section=section)).order_by('title')
        serializer = CostCategoryListSerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request, id_section):
        category = request.data.get('category')
        section = Section.objects.get(pk=id_section, user=request.user)
        serializer = CostCategoryListSerializer(data=category)
        try:
            if serializer.is_valid():
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
        pass

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
        categories = IncomeCategory.objects.filter(Q(section=None) | Q(section=section)).order_by('title')
        serializer = IncomeCategoryListSerializer(categories, many=True)
        return Response({"categories": serializer.data})
