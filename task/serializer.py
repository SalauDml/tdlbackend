from rest_framework import serializers
from .models import Task
from datetime import datetime

#  The Serializers.py file is in charge of converting database code to JSON and vice versa
class TaskSerializer (serializers.ModelSerializer):
    class Meta: 
        model = Task
        fields = '__all__'
        read_only_fields = ['user']

    
    #  The validate function ensures all fields are properly populated and with the right data
    def validate(self,attrs):
        title = attrs.get('title')
        description = attrs.get('description')
        task_complete = attrs.get('task_complete')
        due_date = attrs.get('due_date')

        try:                
            parsed_date = datetime.strptime(due_date,"%Y-%m-%d").date(),due_date
        except TypeError:
            parsed_date = due_date
        except ValueError:
            raise serializers.ValidationError({"date":"Date must be in YYYY-MM-DD format"})
        if parsed_date < datetime.today().date():
            raise serializers.ValidationError({"date": "Date cannot be in the past."})
        if self.partial != True:
            if title == None:
                raise serializers.ValidationError('Title is required')
            if description == None:
                raise serializers.ValidationError('Description is required')
            if task_complete == None:
                raise serializers.ValidationError('is_task_complete is required. Expects False or True')
            if due_date == None:
                raise serializers.ValidationError('Due Date is required.')
            
            
        return attrs
    
    #  The create function is in charge of creating ins
    def create(self,validated_data):
        # user = self.context['request'].user
        date_str = self.context.get('request').data.get('due_date')
        parsed_date = datetime.strptime(date_str,"%Y-%m-%d").date()
        return (Task.objects.create(**validated_data))
    
    def update(self, instance, validated_data):
        instance.task = validated_data.get('task',instance.task)
        instance.task_complete = validated_data.get('task_complete',instance.task_complete)
        instance.save()
        return instance



