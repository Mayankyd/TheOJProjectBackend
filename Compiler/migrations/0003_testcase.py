# Generated by Django 5.2.3 on 2025-07-11 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compiler', '0002_problem_example_defaultcode_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField()),
                ('expected_output', models.TextField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='Compiler.problem')),
            ],
        ),
    ]
