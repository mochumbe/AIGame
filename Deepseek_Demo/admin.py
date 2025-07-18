# admin.py
from django.contrib import admin
from .models import DeepSeekAPIKey, Conversation

@admin.register(DeepSeekAPIKey)
class DeepSeekAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_used', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'course_context')
    list_filter = ('course_context', 'timestamp')
    search_fields = ('user_message', 'ai_response')