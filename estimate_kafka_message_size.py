import json
import sys
test_json = {"metadata":{"info":"important info"},"timestamp":"2018-04-06T12:19:38.611Z","content":{"id":"1","name":"name test","objects":[{"id":"1","url":"http://example.com","properties":[{"id":"1","value":"1"}]}]}}

data = test_json
size_of_json = sys.getsizeof(data)
print(size_of_json)
