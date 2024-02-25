from application.jobs.workers import celery
from datetime import datetime
from flask import current_app as app
from application.utils.helpers import automated_mail, send_products, send_bar_plot_pdf
from celery.schedules import crontab

@celery.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # sends engagement_report 
        # Convert IST to UCT
        crontab(0, 0, day_of_month='2'),
        send_bar_plot_pdf_task.s(),
        name = "trying crontab"
    )
    sender.add_periodic_task(
        # sends an automated mail everyday at 5pm
        # crontab(minute = 30, hour = 11),
        crontab(minute=57, hour=9),
        send_mail_task.s(),
        name = "Sending Automated Mail"
    )


@celery.task()
def send_mail_task():
    automated_mail()
    print("mail sent successfully")

@celery.task()
def send_products_csv(email, user_id):
    send_products(email, user_id)
    print("mail sent successfully")


@celery.task()
def send_bar_plot_pdf_task(email, user_id):
    send_bar_plot_pdf(email, user_id)
    print("mail sent successfully")