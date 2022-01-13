from django.core.serializers import serialize
from django.http import HttpResponse
import json
class TweetMixins(object):
    def serialize(self,querry_set):
        json_data = serialize('json', querry_set)
        pdict = json.loads(json_data)
        finallist = []
        for obj in pdict:
            emp_data = obj['fields']
            finallist.append(emp_data)
        json_data = json.dumps(finallist)
        return json_data
    def render_to_http_response(self,json_data,status=200):
        return HttpResponse(json_data,content_type='application/json',status=status)

