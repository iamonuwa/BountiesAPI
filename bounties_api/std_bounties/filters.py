import rest_framework_filters as filters
from std_bounties.models import Bounty, Category


class CategoriesFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'normalized_name': ['exact', 'contains', 'startswith', 'endswith', 'in']
        }



class BountiesFilter(filters.FilterSet):
    categories = filters.RelatedFilter(CategoriesFilter, name='categories', queryset=Category.objects.all())
    bounty_created = filters.DateFilter(name='bounty_created')

    class Meta:
        model = Bounty
        fields = {
            'issuer': ['exact'],
            'fulfillmentAmount': ['exact', 'lt', 'gt', 'lte'],
            'bountyStage': ['exact'],
            'bounty_created': ['lt', 'gt', 'exact'],
            'deadline': ['lt', 'gt', 'exact'],
        }
