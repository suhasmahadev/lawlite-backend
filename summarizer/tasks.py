import logging
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from .models import Document, ProcessingJob, Summary
from .utils.ml import summarize_text

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def run_ingest_job(self, job_id: int):
    """
    Celery task: send uploaded document to external ML service,
    save the summary, and update job/document status.
    """
    job = ProcessingJob.objects.select_related("document").get(id=job_id)
    doc = job.document

    job.status = "running"
    job.started_at = timezone.now()
    job.save(update_fields=["status", "started_at"])

    try:
        # Read uploaded file
        file_bytes = doc.file.read()
        mimetype = doc.mimetype

        # 🚀 Send to external ML (placeholder)
        summary_text = summarize_text(file_bytes, mimetype)

        with transaction.atomic():
            doc.status = "ready"
            doc.text = ""  # we’re not parsing locally
            doc.last_error = ""
            doc.save(update_fields=["status", "text", "last_error", "updated_at"])

            Summary.objects.create(
                document=doc,
                model="external-ml",
                prompt_version="v1",
                text=summary_text,
                coverage=100.0,
            )

        job.status = "succeeded"
        job.finished_at = timezone.now()
        job.save(update_fields=["status", "finished_at"])

    except Exception as e:
        logger.exception("Ingest job failed")

        doc.status = "failed"
        doc.last_error = str(e)
        doc.save(update_fields=["status", "last_error", "updated_at"])

        job.status = "failed"
        job.error = str(e)
        job.finished_at = timezone.now()
        job.save(update_fields=["status", "error", "finished_at"])
