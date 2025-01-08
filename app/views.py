import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
import json


@csrf_exempt
def proxy_view(request):
    # Handle OPTIONS request
    if request.method == "OPTIONS":
        response = HttpResponse()
        response["Allow"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    # Get the target URL from query parameters
    target_url = request.GET.get("target_url")
    if not target_url:
        return JsonResponse({"error": "Target URL is required"}, status=400)

    # Prepare headers from the original request
    headers = {
        "Content-Type": request.headers.get("Content-Type"),
        "User-Agent": request.headers.get("User-Agent"),
    }

    # Remove 'target_url' from the query parameters
    query_params = request.GET.copy()
    query_params.pop("target_url", None)

    # Prepare the query string without 'target_url'
    filtered_query_string = urlencode(query_params)

    # Extract body (for POST/PUT)
    body = None
    content_type = headers["Content-Type"] if headers["Content-Type"] else ""
    if request.body:
        try:
            body = (
                json.loads(request.body.decode("utf-8"))
                if "application/json" in content_type
                else request.body.decode("utf-8")
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    final_url = f"{target_url}?{filtered_query_string}" if filtered_query_string else target_url

    # Handle different HTTP methods and proxy the request
    try:
        response = {"GET": requests.get, "POST": requests.post, "PUT": requests.put, "DELETE": requests.delete}.get(
            request.method
        )(final_url, headers=headers, data=body)

        # Check content type and return appropriate response
        if response.headers.get("Content-Type") == "application/json":
            return JsonResponse(response.json(), status=response.status_code)
        else:
            return HttpResponse(
                response.content, status=response.status_code, content_type=response.headers.get("Content-Type")
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
