from django.contrib.auth.models import User
from django.db import models

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    acceptance = models.FloatField()
    #solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem')
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"TestCase for {self.problem.title}"

class SolvedProblem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem')
class Example(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='examples')
    input = models.TextField()
    output = models.TextField()
    explanation = models.TextField(blank=True)


class Constraint(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='constraints')
    text = models.CharField(max_length=255)


class DefaultCode(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name='default_code')
    python = models.TextField()
    java = models.TextField()
    cpp = models.TextField()


class CodeSubmission(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
