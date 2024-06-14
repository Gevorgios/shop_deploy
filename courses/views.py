from typing import Any
from django.urls import reverse
from django.shortcuts import render
from .models import Course, Lesson
from django.views.generic import ListView, DetailView
from django.conf import settings
from yookassa import Configuration, Payment


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx


def tarrifsPage(request):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY   
    
    payment = Payment.create({
        "amount": {
            "value": "1500.00",  # Укажите здесь стоимость подписки
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse('home'))  # URL для перенаправления после оплаты на главную страницу
        },
        "description": "Подписка на сайт"
    })
    
    payment_url = payment.confirmation.confirmation_url
    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайте', 'payment_url': payment_url})






class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        ctx['title'] = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['lessons'] = Lesson.objects.filter(course=ctx['title']).order_by('number')
        # print(ctx['lessons'].query)
        return ctx
    
class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lessons-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = list(Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).values())
        # print(ctx['lessons'].query)
        ctx['title'] = lesson[0]['title']
        ctx['desc'] = lesson[0]['description']
        ctx['video'] = lesson[0]['video_url'].split("=")[1]
        return ctx
    

