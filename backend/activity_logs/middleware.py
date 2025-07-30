from activity_logs.utils.create_system_activity import create_system_activity


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)

        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            try:
                view_func = request.resolver_match.func
                view_class = getattr(view_func, "view_class", None) or getattr(view_func, "cls", None)
                activity_map = getattr(view_class, "activtiy_map", None)
                message = activity_map.get(request.method.upper(), None)

                if message == "Login." and response.status_code == 200:
                    # Login activity is handled separately in the LoginViewSet
                    return response

                create_system_activity(
                    user=user,
                    actions=request.method,
                    status_code=response.status_code,
                    message=message or "No message.",
                )

            except Exception as e:
                print(f"[ActivityLog Error] {e}")

        return response
