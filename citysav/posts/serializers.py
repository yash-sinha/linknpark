from rest_framework import serializers
from posts.models import Member, Post, Comment, Upvote, Authority, MemberActivity, Support, NotificationArea


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('email', 'name', 'phone_number', 'karma_points',
                  'profile_picture', 'role')

    def create(self, validated_data):
        name = validated_data.get('name', None)
        email = validated_data.get('email', None)
        phone_number = validated_data.get('phone_number', None)
        profile_picture = validated_data.get('profile_picture', None)
        return Member.objects.create(
            email=email,
            name=name,
            phone_number=phone_number,
            profile_picture=profile_picture)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'lat', 'lon', 'email', 'category',
                  'is_otherCategory', 'upvotes', 'timestamp', 'is_anonymous',
                  'views', 'status', 'verified')

    def create(self, validated_data):
        id = validated_data.get('id', None)
        title = validated_data.get('title', None)
        desc = validated_data.get('desc', None)
        lat = validated_data.get('lat', None)
        lon = validated_data.get('lon', None)
        email = validated_data.get('email', None)
        category = validated_data.get('category', None)
        is_otherCategory = validated_data.get('is_otherCategory', None)
        is_anonymous = validated_data.get('is_anonymous', None)
        verified = validated_data.get('verified', None)
        return Post.objects.create(
            id=id,
            title=title,
            desc=desc,
            lat=lat,
            lon=lon,
            email=email,
            category=category,
            is_otherCategory=is_otherCategory,
            is_anonymous=is_anonymous,
            verified=verified)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_id', 'post_id', 'email', 'comment_text',
                  'timestamp')

    def create(self, validated_data):
        comment_id = validated_data.get('comment_id', None)
        post_id = validated_data.get('post_id', None)
        email = validated_data.get('email', None)
        comment_text = validated_data.get('comment_text', None)
        return Comment.objects.create(
            comment_id=comment_id,
            post_id=post_id,
            email=email,
            comment_text=comment_text)


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = ('email', 'name', 'phone_number', 'location', 'department')

    def create(self, validated_data):
        return Authority.objects.create(**validated_data)
        # TODO : ridz verify if this works


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ('upvote_id', 'post_id', 'email')

    def create(self, validated_data):
        upvote_id = validated_data.get('upvote_id', None)
        post_id = validated_data.get('post_id', None)
        email = validated_data.get('email', None)
        return Upvote.objects.create(
            upvote_id=upvote_id, post_id=post_id, email=email)


class MemberActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberActivity
        fields = ('activity_id', 'email', 'activity_done', 'timestamp')

    def create(self, validated_data):
        activity_id = validated_data.get('activity_id', None)
        email = validated_data.get('email', None)
        activity_done = validated_data.get('activity_done', None)
        return MemberActivity.objects.create(
            activity_id=activity_id, email=email, activity_done=activity_done)


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('support_id', 'email', 'message')

    def create(self, validated_data):
        support_id = validated_data.get('support_id', None)
        email = validated_data.get('email', None)
        message = validated_data.get('message', None)
        return Support.objects.create(
            support_id=support_id, email=email, message=message)


class NotificationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationArea
        fields = ('notification_id', 'email', 'cen_lat', 'cen_lon', 'radius',
                  'user_set')

    def create(self, validated_data):
        notification_id = validated_data.get('notification_id', None)
        email = validated_data.get('email', None)
        cen_lat = validated_data.get('cen_lat', None)
        cen_lon = validated_data.get('cen_lon', None)
        radius = validated_data.get('radius', None)
        user_set = validated_data.get('user_set', None)
        return NotificationArea.objects.create(
            notification_id=notification_id,
            email=email,
            cen_lat=cen_lat,
            cen_lon=cen_lon,
            radius=radius,
            user_set=user_set)
