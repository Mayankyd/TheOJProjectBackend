from django.contrib import admin
from .models import Problem, Example, Constraint, DefaultCode, TestCase

# Inlines
class ExampleInline(admin.TabularInline):
    model = Example
    extra = 1

class ConstraintInline(admin.TabularInline):
    model = Constraint
    extra = 1

class DefaultCodeInline(admin.StackedInline):
    model = DefaultCode
    max_num = 1

class TestCaseInline(admin.TabularInline):  # ✅ NEW INLINE
    model = TestCase
    extra = 1

# Admin config
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'acceptance')
    inlines = [ExampleInline, ConstraintInline, DefaultCodeInline, TestCaseInline]  # ✅ Include it here
