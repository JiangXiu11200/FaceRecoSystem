from activity_logs.models import SystemActivtiyLogs
from django.utils.timezone import now


def create_system_activity(user: str, actions: str, status_code: int, activity: str, message: str = None) -> bool:
    """
    Create a system activity log entry.
    """
    try:
        SystemActivtiyLogs.objects.create(
            account=user,
            actions=actions,
            status=status_code < 400,
            status_code=status_code,
            activity=activity,
            message=message,
            timestamp=now(),
        )
    except Exception as e:
        print(f"[System Activity Log Error] {e}")
        return False
    return True
