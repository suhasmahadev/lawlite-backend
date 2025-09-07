from django.db import models

# Create your models here.
# summarizer/models.pyfrom django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]

    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=512, blank=True, default="")
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    mimetype = models.CharField(max_length=128, blank=True, default="")
    size_bytes = models.BigIntegerField(default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="uploaded")
    extracted_text = models.TextField(blank=True, default="")
    summary_text = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_error = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.id} - {self.title or self.file.name}"

class Summary(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="summaries")
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Summary of {self.document_id} ({self.created_at})"
class ProcessingJob(models.Model):
    """
    Tracks background Celery jobs for document ingestion/summarization.
    """

    JOB_TYPES = [
        ("ingest", "Ingest"),
        ("summarize", "Summarize"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ]

    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="jobs")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    error = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_job_type_display()} for {self.document.title} ({self.status})"