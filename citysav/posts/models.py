from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from enums.member_enums import MemberRoleEnum
from enums.post_enums import PostStatusEnum


class Member(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    karma_points = models.IntegerField(default=50)
    profile_picture = models.TextField(blank=True)
    role = models.CharField(max_length=20, default=MemberRoleEnum.user.name)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    desc = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    email = models.ForeignKey(Member)
    category = models.TextField()
    is_otherCategory = models.BooleanField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default=PostStatusEnum.Review.name)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post)
    email = models.ForeignKey(Member)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.comment_text

    def __str__(self):
        return self.comment_text


class Authority(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email


class Upvote(models.Model):
    upvote_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post)
    email = models.ForeignKey(Member)


class Image(models.Model):
    image = models.ImageField(
        upload_to=settings.IMAGE_UPLOAD_DIR, null=True, blank=True)
    post_id = models.ForeignKey(Post)

    def __unicode__(self):
        return self.image.url

    def __str__(self):
        return self.image.url


class MemberActivity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(Member)
    activity_done = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class NotificationArea(models.Model):
    notification_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    cen_lat = models.FloatField()
    cen_lon = models.FloatField()
    radius = models.FloatField()
    user_set = models.BooleanField(default=False)


class Support(models.Model):
    support_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(Member)
    message = models.TextField()


class Thumbnail(models.Model):
    image = models.ImageField(
        upload_to=settings.IMAGE_THUMBNAIL_DIR, null=True, blank=True)
    post_id = models.ForeignKey(Post)
    status = models.CharField(max_length=20)
    img_id = models.ForeignKey(Image)

    def __unicode__(self):
        return self.image.url

    def __str__(self):
        return self.image.url
