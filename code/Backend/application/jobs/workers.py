from celery import Celery
from flask import current_app as app

celery = Celery("Application Jobs")

# Create a sublcass of the task
# Such that it wraps around the task in an application context

class ContextTasK(celery.Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)