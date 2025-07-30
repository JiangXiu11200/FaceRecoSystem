from activity_logs.utils.create_system_activity import create_system_activity


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            try:
                view_func = request.resolver_match.func
                view_class = getattr(view_func, "view_class", None) or getattr(view_func, "cls", None)
                activity_map = getattr(view_class, "activity_logs", None)
                if not activity_map:
                    return response
                activity = activity_map.get(request.method.upper(), None)

                if activity == "Login." and response.status_code == 200:
                    # Login activity is handled separately in the LoginViewSet
                    return response

                errors = None
                if response.status_code >= 400:
                    errors = next(iter(response.data.values()))
                    # FIXME: 修正 Response message, 回傳格式統一或新增過濾方法

                create_system_activity(
                    user=user,
                    actions=str(request.method),
                    status_code=int(response.status_code),
                    message=errors,
                    activity=activity,
                )

            except Exception as e:
                print(f"[ActivityLog Error] {e}")

        return response
