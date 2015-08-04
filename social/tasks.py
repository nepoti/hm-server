from __future__ import absolute_import
from celery import Celery
from PIL import Image
from urllib2 import urlopen
from StringIO import StringIO
from boto import s3
from boto.s3.key import Key
import constants as c
import user.models

app = Celery('tasks', backend='amqp', broker='amqp://')
client = s3.connect_to_region(c.S3_REGION, host=c.S3_HOST)
bucket = client.get_bucket(c.S3_BUCKET)


@app.task(ignore_result=True, name='tasks.crop_user_image')
def crop_userprofile_image(user_id):
    profile = user.models.UserProfile.objects.filter(id=user_id)
    if not profile.exists():
        return
    profile = profile[0]
    if not profile.user.is_active:
        return
    todo = profile.profile_image
    new_url = todo[1][:-4] + '_m.jpg'
    if todo[0] == new_url:
        return
    # start working
    img = urlopen(todo[1])
    buff = StringIO()
    buff.write(img.read())
    buff.seek(0)
    img = Image.open(buff)
    img.thumbnail((200, 200))
    buff = StringIO()
    img.save(buff, 'JPEG')
    # upload to s3
    k = Key(bucket)
    k.key = todo[1][-68:-4] + '_m.jpg'
    k.set_contents_from_string(buff.getvalue(), headers={'Content-Type': 'image/jpeg'})
    profile.profile_image[0] = new_url
    profile.save()
