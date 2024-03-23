import ipinfo
from .distance import calculate_distance

def time_calculate(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip == '127.0.0.1': # Only define the IP if you are testing on localhost.
        ip = '8.8.8.8'

    shop_ip = '27.123.253.161'
    user_ip = ip
    access_token = 'ffe413e672a58f'
    handler = ipinfo.getHandler(access_token= access_token)
    details1 = handler.getDetails(shop_ip)
    details2 = handler.getDetails(user_ip)
    point1 = details1.loc.split(',')
    point2 = details2.loc.split(',')
    distance = calculate_distance(float(point1[0]), float(point1[1]), float(point2[0]), float(point2[1]))
    minutes = distance * 5
    day = int((minutes / 60) / 12)
    return day