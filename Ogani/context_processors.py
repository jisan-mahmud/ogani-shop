from shop.models import ShopInfo

def shop_info(request):
    info = ShopInfo.objects.get(id= 1)
    return dict(shop_info= info)