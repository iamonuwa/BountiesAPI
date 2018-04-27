from datetime import datetime, date
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import BountiesTimelineSerializer
from .models import BountiesTimeline


class TimelineBounties(APIView):
    def get(self, request):
        since = request.query_params.get('since', "")
        until = request.query_params.get('until', datetime.now().date())

        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()

            if type(until) is not date:
                until_date = datetime.strptime(until, "%Y-%m-%d").date()
            else:
                until_date = until

            if type(since_date) is date and type(until_date) is date:
                bounties_timeline = BountiesTimeline.objects.filter(date__range=[since_date, until_date])
                serialized = BountiesTimelineSerializer(bounties_timeline, many=True)

                return Response(serialized.data)
        except ValueError:
            pass

        res = {"error": 400, "message": "The fields since & until needs being formated as YYYY-MM-DD"}
        return Response(json.dumps(res), status=status.HTTP_200_OK)




