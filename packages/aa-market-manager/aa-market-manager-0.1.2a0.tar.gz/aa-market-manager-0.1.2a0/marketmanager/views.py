from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from esi.decorators import token_required
from django.shortcuts import render, redirect
from django.db.models import QuerySet, Avg, Max, Min, Sum
from eveuniverse.models import EveEntity, EveMarketGroup, EveRegion, EveType
from marketmanager.models import Order, Structure
import datetime
import json

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)

CHARACTER_SCOPES = [
    'esi-markets.read_character_orders.v1',
    'esi-markets.structure_markets.v1',
    'esi-universe.read_structures.v1',
]

CORPORATION_SCOPES = [
    'esi-markets.read_corporation_orders.v1',
    'esi-markets.structure_markets.v1',
    'esi-characters.read_corporation_roles.v1',
    'esi-corporations.read_structures.v1',
    'esi-universe.read_structures.v1',
]


@login_required
@permission_required("marketmanager.view_marketbrowser")
def marketbrowser(request):
    region_id = request.GET.get('region_id', None)
    type_id = request.GET.get('type_id', None)
    all_regions = EveRegion.objects.all()
    all_market_groups = EveMarketGroup.objects.all()

    try:
        eve_type, eve_type_fetched = EveType.objects.get_or_create_esi(id=type_id)
    except Exception:
        eve_type = None

    try:
        eve_region, everegion_fetched = EveRegion.objects.get_or_create_esi(id=region_id)
    except Exception:
        eve_region = None

    if eve_region is None:
        sell_orders = Order.objects.filter(
            eve_type=type_id,
            is_buy_order=False)

    else:
        sell_orders = Order.objects.filter(
            eve_type=type_id,
            eve_region=region_id,
            is_buy_order=False)

    sell_order_stats = order_stats(sell_orders)

    for order in sell_orders:
        # Need to calculate/resolve some fields here
        order.location_resolved = location_resolver(order.location_id)
        order.expiry_calculated = order.issued + datetime.timedelta(days=order.duration)

    if eve_region is None:
        buy_orders = Order.objects.filter(
            eve_type=type_id,
            is_buy_order=True
            )

    else:
        buy_orders = Order.objects.filter(
            eve_type=type_id,
            eve_region=region_id,
            is_buy_order=True
            )

    buy_order_stats = order_stats(buy_orders)

    for order in buy_orders:
        # Need to calculate/resolve some fields here
        order.location_resolved = location_resolver(order.location_id)
        order.expiry_calculated = order.issued + datetime.timedelta(days=order.duration)

    render_items = {
        "all_regions": all_regions,
        "all_market_groups": all_market_groups,
        "eve_region": eve_region,
        "eve_type": eve_type,
        "sell_orders": sell_orders,
        "buy_orders": buy_orders,
        "sell_order_stats": sell_order_stats,
        "buy_order_stats": buy_order_stats}
    return render(request, "marketmanager/marketbrowser.html", render_items)


@login_required
@permission_required("marketmanager.view_marketbrowser")
def marketbrowser_autocomplete(request):
    if request.is_ajax():
        search_query = request.GET.get('term')

    autocomplete_query = EveType.objects.filter(name__istartswith=search_query)
    result = []
    for possible in autocomplete_query:
        data = {}
        data['label'] = possible.name
        data['value'] = possible.id
        result.append(data)
    dump = json.dumps(result)

    mimetype = 'application/json'
    return HttpResponse(dump, mimetype)


@login_required
@permission_required("marketmanager.view_marketbrowser")
def item_selector(request):
    data = EveMarketGroup.objects.all()
    return render(request, "marketmanager/item_selector.html", data)


@login_required
@token_required(scopes=CHARACTER_SCOPES)
def add_char(request, token):
    return redirect('marketmanager:marketbrowser')


@login_required
@token_required(scopes=CORPORATION_SCOPES)
def add_corp(request, token):
    return redirect('marketmanager:marketbrowser')


def location_resolver(location_id):
    if location_id >= 60000000 and location_id <= 64000000:
        # EveStation (Range: 60000000 - 64000000)
        # EveEntity has its own resolver
        # but i dont want Structures to slip through
        # and spam ESI errors
        return EveEntity.objects.resolve_name(location_id)
    else:
        try:
            return Structure.objects.get(structure_id=location_id).name
        except Exception as e:
            logger.error(e)
            return location_id


def order_stats(orders):
    # Returns a specific set of stats for the item_details template
    fifth_percentile = "Fifth Percentile FAKE"
    weighted_average = "Weighted Average Fake"
    median = "Median Fake"
    volume = orders.aggregate(volume=Sum('volume_remain'))["volume"]
    return {
        "fifth_percentile": fifth_percentile,
        "weighted_average": weighted_average,
        "median": median,
        "volume": volume}
