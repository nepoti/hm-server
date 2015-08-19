from __future__ import absolute_import
from celery import Celery
from PIL import Image
from urllib2 import urlopen
from StringIO import StringIO
from boto import s3
from boto.s3.key import Key
import constants as c
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template import loader
from django.core.mail import EmailMultiAlternatives

app = Celery('tasks', backend='amqp', broker='amqp://')
client = s3.connect_to_region(c.S3_REGION, host=c.S3_HOST)
bucket = client.get_bucket(c.S3_BUCKET)


@app.task(ignore_result=True, name='tasks.crop_user_image')
def crop_userprofile_image(user_id):
    from user.models import UserProfile  # circular dependency hell
    profile = UserProfile.objects.filter(id=user_id)
    if not profile.exists():
        return
    profile = profile[0]
    todo = profile.profile_image
    new_url = image_crop(todo[1], todo[0], c.UserProfile_PREVIEW_SIZE)
    if new_url:
        profile.profile_image[0] = new_url
        profile.save()


@app.task(ignore_result=True, name='tasks.crop_post_image')
def crop_post_image(post_id):
    from social.models import Post  # circular dependency hell
    post = Post.objects.filter(id=post_id)
    if not post.exists():
        return
    post = post[0]
    save = False
    for x in range(len(post.photos)):
        photo = post.photos[x]
        new_url = image_crop(photo[1], photo[0], c.POST_PREVIEW_SIZE)
        if new_url:
            save = True
            post.photos[x][0] = new_url
    if save:
        post.save()


@app.task(ignore_result=True, name='tasks.crop_comment_image')
def crop_comment_image(comment_id):
    from social.models import PostComment  # circular dependency hell
    comment = PostComment.objects.filter(id=comment_id)
    if not comment.exists():
        return
    comment = comment[0]
    save = False
    for x in range(len(comment.photos)):
        photo = comment.photos[x]
        new_url = image_crop(photo[1], photo[0], c.COMMENT_PREVIEW_SIZE)
        if new_url:
            save = True
            comment.photos[x][0] = new_url
    if save:
        comment.save()


def image_crop(original_url, current_preview_url, preview_size):
    if not original_url:
        return
    new_url = original_url[:-4] + '_m.jpg'
    if current_preview_url == new_url:
        return
    # start working
    img = urlopen(original_url)
    buff = StringIO()
    buff.write(img.read())
    buff.seek(0)
    img = Image.open(buff)
    img.thumbnail(preview_size)
    buff = StringIO()
    img.save(buff, 'JPEG', optimize=True)
    # upload to s3
    k = Key(bucket)
    k.key = new_url[-70:]
    k.set_contents_from_string(buff.getvalue(), headers={'Content-Type': 'image/jpeg'})
    return new_url


@app.task(ignore_result=True, name='tasks.send_reset_mail')
def send_reset_mail(email):
    from django.contrib.auth.models import User
    domain_override = None
    use_https = False
    template_name = 'reset.html'
    email_template_name = 'reset_email.html'
    subject_template_name='reset_subject.txt'
    for user in User.objects.filter(email__iexact=email, is_active=True):
        site_name = domain = 'dev.it-open.com:8037'
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        send_mail(subject_template_name, email_template_name, context,
                  'TheHealth.me <noreply@thehealth.me>', user.email)


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
