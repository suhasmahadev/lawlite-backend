from django.contrib import admin
from .models import Document, Summary, ProcessingJob

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'owner__username', 'file', 'status')
    readonly_fields = ('created_at', 'updated_at', 'last_error')

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'created_at')
    search_fields = ('document__title',)

@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'job_type', 'status', 'created_at')
    search_fields = ('document__title', 'job_type', 'status')
    readonly_fields = ('created_at', 'started_at', 'finished_at')
