from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import UserProfile
from response.templates import invalid_data, access_error, ok_response, status_ok


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, related_name='posts')
    text = models.CharField(blank=True, default=u'', max_length=1000)
    photos = ArrayField(models.URLField(), max_length=10)
    locations = ArrayField(ArrayField(models.FloatField(), size=2), max_length=10)

    @staticmethod
    def get_post(post_id):
        q = Post.objects.filter(id=post_id)
        if not q.exists():
            return invalid_data
        q = q[0]
        return ok_response([{'id': q.id, 'timestamp': q.timestamp, 'author': q.author.id,
                             'text': q.text, 'photos': q.photos, 'locations': q.locations, 'likes': q.likes.count(),
                             'comments': q.comments.count()}])

    @staticmethod
    def create(author, text=None, photos=None, locations=None):
        if text is None and photos is None and locations is None:
            return invalid_data
        if text is not None:
            if type(text) is not unicode:
                return invalid_data
            elif len(text) > 1000:
                return invalid_data
        else:
            text = u''
        if photos is not None:
            if type(photos) is not list:
                return invalid_data
            elif len(photos) > 10:
                return invalid_data
            else:
                for x in photos:
                    if type(x) != unicode:
                        return invalid_data
                    elif len(x) > 200:
                        return invalid_data
        else:
            photos = []
        if locations is not None:
            if type(locations) is not list:
                return invalid_data
            elif len(locations) > 10:
                return invalid_data
            else:
                for x in locations:
                    if type(x) is not list:
                        return invalid_data
                    elif len(x) != 2:
                        return invalid_data
                    elif type(x[0]) is not float or type(x[1]) is not float:
                        return invalid_data
        else:
            locations = []
        post = Post(author=author, text=text, photos=photos, locations=locations)
        post.save()
        return ok_response([{'id': post.id, 'timestamp': post.timestamp}])

    def edit(self, author, text, photos, locations):
        if text is None and photos is None and locations is None:
            return invalid_data
        if self.author != author:
            return access_error
        if text is not None:
            if type(text) is not unicode:
                return invalid_data
            elif len(text) > 1000:
                return invalid_data
        if photos is not None:
            if type(photos) is not list:
                return invalid_data
            elif len(photos) > 10:
                return invalid_data
            else:
                for x in photos:
                    if type(x) != unicode:
                        return invalid_data
                    elif len(x) > 200:
                        return invalid_data
        if locations is not None:
            if type(locations) is not list:
                return invalid_data
            elif len(locations) > 10:
                return invalid_data
            else:
                for x in locations:
                    if type(x) is not list:
                        return invalid_data
                    elif len(x) != 2:
                        return invalid_data
                    elif type(x[0]) is not float or type(x[1]) is not float:
                        return invalid_data
        if text:
            self.text = text
        if photos:
            self.photos = photos
        if locations:
            self.locations = locations
        self.save()
        return status_ok

    def remove(self, author):
        if self.author != author:
            return access_error
        self.author.posts.filter(id=self.id)[0].delete()
        return status_ok


class PostComment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile)
    text = models.CharField(blank=True, default=u'', max_length=500)
    photos = ArrayField(models.URLField(), max_length=10)
    locations = ArrayField(ArrayField(models.FloatField(), size=2), max_length=10)
    post = models.ForeignKey(Post, related_name='comments')

    @staticmethod
    def get_comment(comment_id):
        q = PostComment.objects.filter(id=comment_id)
        if not q.exists():
            return invalid_data
        q = q[0]
        return ok_response([{'id': q.id, 'timestamp': q.timestamp, 'post': q.post.id, 'author': q.author.id,
                             'text': q.text, 'photos': q.photos, 'locations': q.locations, 'likes': q.likes.count()}])

    @staticmethod
    def create(post, author, text, photos, locations):
        if text is None and photos is None and locations is None:
            return invalid_data
        if text is not None:
            if type(text) is not unicode:
                return invalid_data
            elif len(text) > 500:
                return invalid_data
        else:
            text = u''
        if photos is not None:
            if type(photos) is not list:
                return invalid_data
            elif len(photos) > 10:
                return invalid_data
            else:
                for x in photos:
                    if type(x) != unicode:
                        return invalid_data
                    elif len(x) > 200:
                        return invalid_data
        else:
            photos = []
        if locations is not None:
            if type(locations) is not list:
                return invalid_data
            elif len(locations) > 10:
                return invalid_data
            else:
                for x in locations:
                    if type(x) is not list:
                        return invalid_data
                    elif len(x) != 2:
                        return invalid_data
                    elif type(x[0]) is not float or type(x[1]) is not float:
                        return invalid_data
        else:
            locations = []
        comment = PostComment(post=post, author=author, text=text, photos=photos, locations=locations)
        comment.save()
        return ok_response([{'id': comment.id, 'timestamp': comment.timestamp}])

    def edit(self, author, text, photos, locations):
        if text is None and photos is None and locations is None:
            return invalid_data
        if self.author != author:
            return access_error
        if text is not None:
            if type(text) is not unicode:
                return invalid_data
            elif len(text) > 500:
                return invalid_data
        if photos is not None:
            if type(photos) is not list:
                return invalid_data
            elif len(photos) > 10:
                return invalid_data
            else:
                for x in photos:
                    if type(x) != unicode:
                        return invalid_data
                    elif len(x) > 200:
                        return invalid_data
        if locations is not None:
            if type(locations) is not list:
                return invalid_data
            elif len(locations) > 10:
                return invalid_data
            else:
                for x in locations:
                    if type(x) is not list:
                        return invalid_data
                    elif len(x) != 2:
                        return invalid_data
                    elif type(x[0]) is not float or type(x[1]) is not float:
                        return invalid_data
        if text:
            self.text = text
        if photos:
            self.photos = photos
        if locations:
            self.locations = locations
        self.save()
        return status_ok

    def remove(self, author):
        if self.author != author and self.post.author != author:
            return access_error
        self.post.comments.filter(id=self.id)[0].delete()
        return status_ok


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile)
    post = models.ForeignKey(Post, related_name='likes')


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile)
    comment = models.ForeignKey(PostComment, related_name='likes')
