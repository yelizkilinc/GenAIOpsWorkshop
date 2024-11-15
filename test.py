import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data = {
  "question": "what is Lamna Healthcare?",
  "chat_history": []
}


body = str.encode(json.dumps(data))

url = 'https://rag-1039-endpoint.eastus2.inference.ml.azure.com/score'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjNQYUs0RWZ5Qk5RdTNDdGpZc2EzWW1oUTVFMCIsImtpZCI6IjNQYUs0RWZ5Qk5RdTNDdGpZc2EzWW1oUTVFMCJ9.eyJhdWQiOiJodHRwczovL21sLmF6dXJlLmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzE2YjNjMDEzLWQzMDAtNDY4ZC1hYzY0LTdlZGEwODIwYjZkMy8iLCJpYXQiOjE3MzE2Njc0MDEsIm5iZiI6MTczMTY2NzQwMSwiZXhwIjoxNzMxNjcyNTYwLCJhY3IiOiIxIiwiYWlvIjoiQWFRQVcvOFlBQUFBSmp1UGFiQVYvRkU1b2pUY0NFTFJ0blNtYzhrRHZ2akRRaVBFU2JsS250emlkYmU2MzQ1SlV3RFpnUWt5QlpPZENZQjVUK0pXMlRwaFVYVEVORzFuNEtRTklncFRtNUQyejlJTFJ5Y1FpVlVRc05uS1B0d3J2SVdOcWVhT1BVczZVV0pJU05VQ05pQjAzR1RJSGNadjQweGVsTmRjRTMzbjREdVFLM21qZURGaGNvR0VpZmFqYlBrdGlWVVZjQ25KQzV4ZHh2aVREZzE5ZWg3QkUyTzFDQT09IiwiYWx0c2VjaWQiOiI1OjoxMDAzMjAwMUVEMUI1NDlDIiwiYW1yIjpbInJzYSIsIm1mYSJdLCJhcHBpZCI6ImNiMmZmODYzLTdmMzAtNGNlZC1hYjg5LWEwMDE5NGJjZjZkOSIsImFwcGlkYWNyIjoiMCIsImRldmljZWlkIjoiNjBmMjQzMTQtYjFmYy00N2FkLWE4Y2UtYjc3MDM4NjBkMjk5IiwiZW1haWwiOiJ5ZWxpemtpbGluY0BtaWNyb3NvZnQuY29tIiwiZmFtaWx5X25hbWUiOiJLaWxpbmMiLCJnaXZlbl9uYW1lIjoiWWVsaXoiLCJncm91cHMiOlsiYjEzMDQwMjItMDhlNi00NDdkLWIwOTQtMTUzNzA1OTdjNmI2IiwiMDk1MzFhNzItMmMzZS00ZTA2LWJlMWUtMjU5NmJkMDhkY2RkIiwiZDM0YzRlYmUtNDk4NC00OTAzLWE2NGQtOGMyMDI4M2Q1MTZiIiwiZTMwOTZkZjctYjY1Yy00ZTMyLWFiMWEtN2EzNWRjNjg0ZjBhIl0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiI3OC4xNTAuMTQzLjE3OCIsIm5hbWUiOiJZZWxpeiBLaWxpbmMiLCJvaWQiOiI2ZjA3ZTE4ZC03ZjJjLTQ1YTUtOGM0Ni1kZDBlYjhkZDhiMGUiLCJwdWlkIjoiMTAwMzIwMDIyNjI3OEUyQyIsInJoIjoiMS5BVVlBRThDekZnRFRqVWFzWkg3YUNDQzIwMTl2cGhqZjJ4ZE1uZGNXTkhFcW5MN3hBQnhHQUEuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoiZ0RsOHdhTFppRmY5aHl2a2llRkdJNlRnaWN0S3pFUU83dWlSYTJkM21WZyIsInRpZCI6IjE2YjNjMDEzLWQzMDAtNDY4ZC1hYzY0LTdlZGEwODIwYjZkMyIsInVuaXF1ZV9uYW1lIjoieWVsaXpraWxpbmNAbWljcm9zb2Z0LmNvbSIsInV0aSI6IldtdHY3cjc3SzBPb0RaWndiRE15QUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfaWRyZWwiOiIyMCAxIn0.GBGNIPlt3HdsX3t8JRWqVmXeLf5vO_dP8b24yhWpGkabXrFK9u4zS9-OfXwXs5O76gNoO7zw_5_rkHk4jM62imiF_YrJTRsm20QSwNwgllUBKEk38WOpIc6D-EmKAK5bkFMw6_iGYIIYN0PHb7LNqTHtZ2_FjkZkNe3Zt0v0zhP6J4lVM7i0ELzLGFPy5nxCbbA4sdSHiOXG4TWMZVfNBUKh_zc7hBZQRlEj6eBjftjjgCNYVd7zMbCytdgYi2puanCDAf6pdIapVxrJNZTyM7VG9CPex3YRZOhOoT2VCtv5i-vsl-v6TfAXLJSwDvwUPt-RKFgnac2zQ8T19MelDg'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))