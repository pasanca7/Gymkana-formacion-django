from portal.models import New
from django.utils import timezone
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'portal/index.html'
    context_object_name = 'lastest_news_list'

    def get_queryset(self):
        """
    Just a Test. Showing the news
    """
        return New.objects.filter(publish_date__lte = timezone.now()).order_by('-publish_date')[:5]
