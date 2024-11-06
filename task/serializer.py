from rest_framework import serializers
from .models import Task

class TaskSerializer (serializers.ModelSerializer):
    class Meta: 
        model = Task
        fields = '__all__'
        read_only_fields = ['user']
    
    def validate(self,attrs):
        title = attrs.get('title')
        description = attrs.get('description')
        task_complete = attrs.get('task_complete')
        if self.partial != True:
            if not title:
                raise serializers.ValidationError('Title is needed')
            if not description:
                raise serializers.ValidationError('Description is needed')
            if not task_complete:
                raise serializers.ValidationError('is task complete is needed')
        return attrs

    def create(self,validated_data):
        # user = self.context['request'].user
        return (Task.objects.create(**validated_data))
    
    def update(self, instance, validated_data):
        instance.task = validated_data.get('task',instance.task)
        instance.task_complete = validated_data.get('task_complete',instance.task_complete)
        instance.save()
        return instance



