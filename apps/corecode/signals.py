from django.db.models.signals import post_save
from django.dispatch import receiver
from .email import send_html_email_async

from .models import AcademicSession, AcademicTerm, CustomerDetail


@receiver(post_save, sender=AcademicSession)
def after_saving_session(sender, created, instance, *args, **kwargs):
    """Change all academic sessions to false if this is true"""
    if instance.current is True:
        AcademicSession.objects.exclude(pk=instance.id).update(current=False)


@receiver(post_save, sender=AcademicTerm)
def after_saving_term(sender, created, instance, *args, **kwargs):
    """Change all academic terms to false if this is true."""
    if instance.current is True:
        AcademicTerm.objects.exclude(pk=instance.id).update(current=False)

@receiver(post_save,sender=CustomerDetail)
def after_saving_customerdetail(sender,created,instance, *args, **kwargs):
    send_html_email_async(subject='New Form has been submitted',to_emails=['shekharanand7773@gmail.com'], content_context={})

