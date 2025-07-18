# admin.py
from django.contrib import admin
from .models import DeepSeekAPIKey, Conversation

@admin.register(DeepSeekAPIKey)
class DeepSeekAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('last_used', 'is_active')
    list_filter = ('is_active',)
    

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'course_context')
    list_filter = ('course_context', 'timestamp')
    