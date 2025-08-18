from celery import shared_task
from utils.minio_client import MinioClient


@shared_task
def cleanup_temporary_data(retention_days: int = 7):
    try:
        cleanup_status, message = MinioClient.cleanup_old_files(
            bucket_name="temporary-data",
            max_age_seconds=retention_days * 24 * 60 * 60,
        )
        if cleanup_status:
            return f"Successfully cleaned up S3 temporary data: {message}"
    except Exception as e:
        return f"Error cleaning up S3 temporary data: {str(e)}"
