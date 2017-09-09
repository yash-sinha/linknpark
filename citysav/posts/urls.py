
from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns

import posts.deprecated_views.views
from posts.new_views import member, post, notification, views


active_urls = [
    # get all posts and create a new post
    url(r'^api/post/$', post.PostList.as_view()),
    # get a post detail , update or delete a post
    url(r'^api/post/(?P<pk>[0-9]+)/$', post.PostDetail.as_view()),
    # get all members and create a new member
    url(r'^api/member/$', member.MemberList.as_view()),
    # get detail of a member, update or delete a member
    url(r'^api/member/(?P<pk>[\w.@+-]+)/$', member.MemberDetail.as_view()),
    url(r'^api/imageUpload/$', post.image_upload,name='image_upload'),
    url(r'^api/getImage/$', post.send_image,name='send_image'),
    # get all comments and create a new comment
    url(r'^api/comment/$', post.CommentList.as_view()),
    url(r'^api/post/comment/$', post.CommentList.as_view()),
    # get all authorities or create a new authority
    url(r'^api/authority/$', views.AuthorityList.as_view()),
    # get detail of an authority or update or delete an authority
    url(r'^api/authority/(?P<pk>[\w.@+-]+)/$', views.AuthorityDetail.as_view()),
    # get all upvotes or create a new upvote
    url(r'^api/postUpvote/$', post.UpvoteList.as_view()),
    # get all upvotes or create a new upvote
    url(r'^api/upvote/$', post.UpvoteList.as_view()),
    url(r'^api/deleteImage/$', post.deleteImage,name='deleteImage'),

    # get all activities or create a new activity
    url(r'^api/postMemberActivity/$', views.MemberActivityList.as_view()),
    # create a new FCM device
    url(r'^api/checkOrCreateFCMDevice/$', views.checkOrCreateFCMDevice,name='checkOrCreateFCMDevice'),
    # get all support messages or create a new one
    url(r'^api/sendSupportMessage/$', views.SupportList.as_view()),

    # send notification to all members of an area
    url(r'^api/send_area_notification/$',notification.send_area_notification,name='send_area_notification'),
    # not tested
    url(r'^api/notification/area/send/$',
        notification.send_area_notification,
        name='send_area_notification'),

    # send notification to a single user
    url(r'^api/send_user_notification/$',notification.send_user_notification,name='send_user_notification'),
    # not tested
    url(r'^api/notification/user/send/$',
        notification.send_user_notification,
        name='send_user_notification'),

    # for testing
    url(r'^api/sendMail/(?P<post>[0-9]+)/$',notification.sendMail,name='sendMail'),
    # for testing
    url(r'^api/send_notification/$', notification.send_notification,name='send_notification'),

    # new urls
    url(r'^api/leaderboard/$', views.get_leaderboard, name='getLeaderboard'),
    url(r'^api/member/rank/(?P<points>[0-9]+)/$', views.get_user_rank, name="getUserRank"),
    url(r'^api/notificationarea/$', notification.NotificationAreaList.as_view()),
    url(r'^api/notificationarea/(?P<pk>[0-9]+)/$', notification.NotificationAreaDetail.as_view()),
    url(r'^api/notificationarea/(?P<email>[\w.@+-]+)/$', notification.getNotificationArea, name="getNotificationArea"),

    url(r'^api/user_post/(?P<email>[\w.@+-]+)/$', post.user_post, name='user_post'),
    url(r'^api/post_nearby/$', post.post_nearby, name='post_nearby'),
    url(r'^api/post/image/get/(?P<post>[0-9]+)/$', post.get_image, name='get_image'),

    url(r'^api/post/comment/(?P<pk>[0-9]+)/$', post.CommentDetail.as_view()),
    url(r'^api/comment/(?P<pk>[0-9]+)/$', post.CommentDetail.as_view()),

    url(r'^api/upvote/check/$', post.upvoteCheck, name="upvoteCheck"),
    url(r'^api/post/getComment/(?P<post_id>[0-9]+)/$', post.getComment, name="getComment"),
    url(r'^api/post/upvote/update/$', post.updatePostUpvote, name='updatePostUpvote'),
    url(r'^api/post/upvote/delete/$', post.deleteUpvote, name='deleteUpvote'),
    url(r'^api/post/views/increase/$', post.increasePostViews, name='increasePostViews'),
    url(r'^api/post/image/thumbnail/$', post.getThumbnail, name="getThumbnail"),

]

deprecated_urls = [
    url(r'^api/post/(?P<email>[\w.@+-]+)/$', posts.deprecated_views.views.post_search, name='post_search'), # deprecated
    url(r'^api/post/(?P<lat>[-+]?\d+[.]*\d*)/(?P<lon>[-+]?\d+[.]*\d*)/$',
        posts.deprecated_views.views.post_search_nearby, name='post_search_nearby'), # deprecated
    url(r'^api/post_search_nearby/$', posts.deprecated_views.views.post_search_nearby1, name='post_search_nearby1'), # deprecated
    url(r'^api/memberupdate/$', posts.deprecated_views.views.member_update, name='member_update'), # deprecated
    url(r'^api/checkUpvote/$', posts.deprecated_views.views.checkUpvote, name='checkUpvote'),  # deprecated
    url(r'^api/getComments/(?P<post_id>[0-9]+)/$', posts.deprecated_views.views.getComments, name='getComments'),  # deprecated
    url(r'^api/updateUpvote/$', posts.deprecated_views.views.updateUpvote, name='updateUpvote'),  # deprecated
    url(r'^api/cancelUpvote/$', posts.deprecated_views.views.cancelUpvote, name='cancelUpvote'),  # deprecated
    url(r'^api/decreaseUpvote/$', posts.deprecated_views.views.decreaseUpvote, name='decreaseUpvote'),  # deprecated
    url(r'^api/deleteComment/$', posts.deprecated_views.views.deleteComment, name='deleteComment'),  # deprecated
    url(r'^api/updateComment/$', posts.deprecated_views.views.updateComment, name='updateComment'),  # deprecated
    url(r'^api/updatePost/$', posts.deprecated_views.views.updatePost, name='updatePost'), # deprecated
    url(r'^api/updateKarma/$', posts.deprecated_views.views.updateKarma, name='updateKarma'),  # deprecated
    url(r'^api/updatePostViews/$', post.updatePostViews, name='updatePostViews'),  # deprecated
    url(r'^api/getLeaderBoard/$', posts.deprecated_views.views.getLeaderBoard, name='getLeaderBoard'),  # deprecated
    url(r'^api/getMyRank/$', posts.deprecated_views.views.getMyRank, name='getMyRank'),  # deprecated
    url(r'^api/createOrUpdateArea/$', notification.createOrUpdateArea, name='createOrUpdateArea'),  # deprecated
    url(r'^api/getArea/(?P<email>[\w.@+-]+)/$', notification.getArea, name='getArea'),  # deprecated

]
urlpatterns = []
urlpatterns.extend(active_urls)
urlpatterns.extend(deprecated_urls)

urlpatterns = format_suffix_patterns(urlpatterns)
