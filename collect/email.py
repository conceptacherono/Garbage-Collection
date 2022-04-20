from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_join_email(name,receiver):
    subject = 'Thankyou for Joining Us'
    sender = 'melody.towett@student.moringaschool.com'
    text_content = render_to_string('email/attend.txt',{"name":name})
    html_content = render_to_string('email/attend.html',{"name":name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()