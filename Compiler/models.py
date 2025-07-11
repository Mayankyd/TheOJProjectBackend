from django.db import models

# Create your models here.

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
    solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
