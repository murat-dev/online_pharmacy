from celery import task
from django.core.mail import send_mail

from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f'Dear {order.first_name},\nYou have successfully placed an order. Your order id is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          'admin@pyteka.com',
                          [order.email])
    return mail_sent
