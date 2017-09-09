
from django.contrib import admin
from .models import Member,Post,Comment,Upvote,Image,Authority,MemberActivity,NotificationArea,Support,Thumbnail
# Register your models here.


class MemberModelAdmin(admin.ModelAdmin):
    list_display=["email","name","phone_number","karma_points","profile_picture"]
    list_filter = ["name"]
    search_fields= ["name","email","phone_number"]

    class Meta:
        model = Member


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","title", "lat", "lon", "email","category","views","status"]
    list_display_links = ["title"]
    list_filter = ["updated", "timestamp","title","status"]
    search_fields = ["title", "desc", "category","status"]

    class Meta:
        model = Post

class CommentModelAdmin(admin.ModelAdmin):
    list_display= ["comment_id","post_id","email","comment_text","timestamp"]
    list_filter = ["post_id","email"]
    search_fields = ["post_id","email"]

    class Meta:
        model = Comment

class AuthorityModelAdmin(admin.ModelAdmin):
    list_display =["email","name","department"]
    list_display_links =["email"]
    list_filter = ["department","location"]
    search_fields = ["department","location"]

    class Meta:
        model = Authority

class UpvoteModelAdmin(admin.ModelAdmin):
    list_display=["upvote_id","post_id","email"]
    list_filter = ["post_id","email"]
    search_fields = ["post_id","email"]

    class Meta:
        model = Upvote

class ImageModelAdmin(admin.ModelAdmin):
    list_display= ["post_id","image"]
    list_filter = ["post_id"]
    search_fields = ["post_id"]

    class Meta:
        model = Image

class MemberActivityAdmin(admin.ModelAdmin):
    list_display = ["email","activity_done"]
    list_filter = ["email","activity_id"]
    search_fields= ["email","activity_id"]

    class Meta:
        model = MemberActivity

class NotificationAreaAdmin(admin.ModelAdmin):
    list_display = ["email","cen_lat","cen_lon","radius"]
    list_filter = ["email"]
    search_fields = ["email"]

    class Meta:
        model = NotificationArea

class SupportAdmin(admin.ModelAdmin):
    list_display = ["email","message"]
    list_filter = ["email"]
    search_fields = ["email"]

    class Meta:
        model = Support

class ThumbnailAdmin(admin.ModelAdmin):
    list_display=["image","post_id","status","img_id"]
    list_filter = ["post_id","img_id"]
    search_fields = ["post_id","img_id"]

    class Meta:
        model = Thumbnail

admin.site.register(Post,PostModelAdmin)
admin.site.register(Member,MemberModelAdmin)
admin.site.register(Comment,CommentModelAdmin)
admin.site.register(Upvote,UpvoteModelAdmin)
admin.site.register(Authority,AuthorityModelAdmin)
admin.site.register(Image,ImageModelAdmin)
admin.site.register(MemberActivity,MemberActivityAdmin)
admin.site.register(NotificationArea,NotificationAreaAdmin)
admin.site.register(Support,SupportAdmin)
admin.site.register(Thumbnail,ThumbnailAdmin)