from rest_framework import serializers
from .models import Problem, Example, Constraint, DefaultCode, TestCase
from django.contrib.auth.models import User
from rest_framework import serializers

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['input', 'output', 'explanation']

class ConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constraint
        fields = ['text']
class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output']
class DefaultCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultCode
        fields = ['python', 'java', 'cpp']

class LeaderboardUserSerializer(serializers.ModelSerializer):
    solved_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'solved_count']
class ProblemSerializer(serializers.ModelSerializer):
    examples = ExampleSerializer(many=True, read_only=True)
    constraints = ConstraintSerializer(many=True, read_only=True)
    defaultCode = DefaultCodeSerializer(source='default_code', read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)# renamed for React compatibility

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'description',
            'difficulty',
            'acceptance',
            'examples',
            'constraints',
            'defaultCode',
            'test_cases'# must match React naming
        ]
