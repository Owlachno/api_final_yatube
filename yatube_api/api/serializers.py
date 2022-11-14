from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title")
        read_only_fields = ("id",)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Вы уже подписаны на этого пользователя!",
            )
        ]

    def validate_following(self, value):
        print(self)
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return value
