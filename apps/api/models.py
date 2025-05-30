from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class APKVersion(models.Model):
    version = models.CharField(max_length=10, unique=True)
    os = models.CharField(max_length=50, choices=(('android','Android'),('ios','iOS')),default="")
    file = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version}"
    

class ErrorLog(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    error = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    app_type = models.IntegerField(choices=[
        (0, '.apk'),
        (1, 'web'),(2, '.ios')],default=0)
    level = models.CharField(max_length=50, choices=[
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ])
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.level} - {self.error}"



class WhatsAppInboundMessage(models.Model):
    # Sender Information
    sender_number = models.CharField(max_length=15, help_text="Phone number of the sender")
    sender_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the sender (if available)")

    # Message Details
    message_id = models.CharField(max_length=255, unique=True, help_text="Unique ID of the message from Infobip")
    message_content = models.TextField(help_text="Content of the WhatsApp message")
    message_type = models.CharField(
        max_length=50, 
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('audio', 'Audio'),
            ('location', 'Location'),
            ('contact', 'Contact'),
            ('sticker', 'Sticker'),
            ('other', 'Other')
        ],
        default='text',
        help_text="Type of the message"
    )

    # Timestamp
    received_at = models.DateTimeField(help_text="Timestamp when the message was received")

    # Metadata
    metadata = models.JSONField(blank=True, null=True, help_text="Additional metadata for the message")

    # Status and Flags
    processed = models.BooleanField(default=False, help_text="Flag to mark if the message has been processed")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record update timestamp")

    def __str__(self):
        return f"Message from {self.sender_number} ({self.message_type})"

    class Meta:
        verbose_name = "WhatsApp Inbound Message"
        verbose_name_plural = "WhatsApp Inbound Messages"
        ordering = ['-received_at']

    def __str__(self):
        return self.message_id

    def get_absolute_url(self):
        return reverse("WhatsAppInboundMessage_detail", kwargs={"pk": self.pk})


class WhatsAppOutboundMessage(models.Model):
    # Recipient Information
    recipient_number = models.CharField(max_length=15, help_text="Phone number of the recipient")
    recipient_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the recipient (if available)")

    # Message Details
    message_id = models.CharField(max_length=255, help_text="Unique ID of the message from Infobip (if available)")
    message_content = models.TextField(help_text="Content of the WhatsApp message")
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('audio', 'Audio'),
            ('location', 'Location'),
            ('contact', 'Contact'),
            ('sticker', 'Sticker'),
            ('template', 'Template'),
            ('other', 'Other')
        ],
        default='text',
        help_text="Type of the message"
    )

    # Status and Metadata
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('failed', 'Failed'),
        ],
        default='pending',
        help_text="Status of the outbound message"
    )
    metadata = models.JSONField(blank=True, null=True, help_text="Additional metadata for the message")

    # Timestamps
    sent_at = models.DateTimeField(blank=True, null=True, help_text="Timestamp when the message was sent")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record update timestamp")

    def __str__(self):
        return f"Message to {self.recipient_number} ({self.message_type}) - {self.status}"

    class Meta:
        verbose_name = "WhatsApp Outbound Message"
        verbose_name_plural = "WhatsApp Outbound Messages"
        ordering = ['-created_at']


class WhatsappDeliveryStatus(models.Model):
    bulk_id = models.CharField(_("Bulk_id"), max_length=550,null=True,blank=True)
    message_id = models.CharField(max_length=255, unique=True)
    to = models.CharField(max_length=20)
    sent_at = models.DateTimeField()
    done_at = models.DateTimeField()
    status_id = models.IntegerField()
    status_group_id = models.IntegerField()
    status_group_name = models.CharField(max_length=50)
    status_name = models.CharField(max_length=50)
    status_description = models.CharField(max_length=255)
    error_id = models.IntegerField()
    error_group_id = models.IntegerField()
    error_group_name = models.CharField(max_length=50)
    error_name = models.CharField(max_length=50)
    error_description = models.CharField(max_length=255)
    error_permanent = models.BooleanField()
    price_per_message = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    class Meta:
        verbose_name = "WhatsApp Delivery Reports"
        verbose_name_plural = "WhatsApp Delivery Reports"
        # ordering = ['-created_at']

class WhatsappSeenReport(models.Model):
    message_id = models.CharField(max_length=255, unique=True)
    sender = models.CharField(max_length=20)
    recipient = models.CharField(max_length=20)
    sent_at = models.DateTimeField()
    seen_at = models.DateTimeField()
    application_id = models.CharField(max_length=255, null=True, blank=True)
    entity_id = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        verbose_name = "WhatsApp Seen Reports"
        verbose_name_plural = "WhatsApp Seen Reports"
        # ordering = ['-created_at']

