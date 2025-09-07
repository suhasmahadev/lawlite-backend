from rest_framework import serializers
from .models import Document, Summary, ProcessingJob

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'owner', 'title', 'file', 'mimetype', 'size_bytes',
            'status', 'extracted_text', 'summary_text', 'created_at', 'updated_at', 'last_error'
        ]
        read_only_fields = ['id', 'owner', 'status', 'extracted_text', 'summary_text', 'created_at', 'updated_at', 'last_error']

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['id', 'document', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProcessingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingJob
        fields = ['id', 'document', 'job_type', 'status', 'error', 'created_at', 'started_at', 'finished_at']
        read_only_fields = ['id', 'created_at', 'started_at', 'finished_at']
