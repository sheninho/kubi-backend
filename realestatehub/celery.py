# # celery.py
# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # Définir la variable d'environnement par défaut pour les paramètres Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestatehub.settings')
#
# app = Celery('realestatehub')
#
# # Utiliser la configuration de la base de données de Django
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Découvrir les tâches automatiquement dans toutes les applications Django inscrites
# app.autodiscover_tasks()
