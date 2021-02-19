from django.db.models import Count, Q

from shop_list.models import TreatBrands


def common(request):
    context = {
        'treatbrnds': TreatBrands.objects.annotate(
            num_posts=Count('brandname')),
    }
    return context