# # tasks.py dans l'une de vos applications Django
# from celery import shared_task
# from django.core.mail import send_mail
#
# @shared_task
# def send_verification_email(code):
#     send_mail(
#         'Votre code de vérification',
#         f'Votre code de vérification est: {code}',
#         'msakande21@gmail.com',
#         ['shunikiema@gmail.com', ],
#         fail_silently=False,
#     )