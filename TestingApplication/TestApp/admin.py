import uuid

from django.contrib import admin
from .models import *

# Регистрация модели Category
admin.site.register(Test)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    filter_horizontal = ('answer_options','right_answers')

    def save_model(self, request, obj, form, change):
        # Сохраняем объект для получения значения ID
        print("**********************************************")
        print("obj = ", obj)
        print("**********************************************")
        if not obj.id:
            obj.id = str(uuid.uuid4())
        super().save_model(request, obj, form, change)

        # Теперь можно работать с ManyToMany полями, поскольку объект уже сохранен и имеет ID
        if form.cleaned_data.get('answers'):
            obj.answers.set(form.cleaned_data['answers'])


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)




admin.site.register(TestPass)

