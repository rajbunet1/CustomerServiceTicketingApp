from random import randint

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    ADMIN_ROLE = "ADMIN"
    CUSTOMER_ROLE = "CUSTOMER"
    REGULAR_ROLE = "REGULAR"

    ROLES_CHOICES = (
        (ADMIN_ROLE, "Admin"),
        (CUSTOMER_ROLE, "Customer"),
        (REGULAR_ROLE, "Regular"),
    )
    role = models.CharField(max_length=10,
                            choices=ROLES_CHOICES)


def customer_phone_number_validator(value):
    if type(value) is str:
        if len(value) == 11 and value[0:2] == "07":
            return value
    raise ValidationError("Ticket number must have 11 digits and start with 07")


def create_customer_phone_number():
    return "07" + str(randint(100000000, 999999999))


class Ticket(models.Model):
    CANCELLED_STATUS = "CANCELLED"
    IN_PROGRESS_STATUS = "IN_PROGRESS"
    REVIEW_STATUS = "REVIEW"
    CLOSED_STATUS = "CLOSED"

    STATUS_CHOICES = (
        (IN_PROGRESS_STATUS, "In progress"),
        (REVIEW_STATUS, "Review"),
        (CLOSED_STATUS, "Closed"),
        (CANCELLED_STATUS, "Cancelled")
    )

    title = models.CharField(max_length=30)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    files = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS_STATUS)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tickets_opened")
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tickets_processed", null=True)
    response = models.TextField(null=True)
    customer_phone_number = models.CharField(max_length=11, default=create_customer_phone_number,
                                             validators=[customer_phone_number_validator])
