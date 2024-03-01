import json

from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from SystemForStudy.models import Product, Lesson, Group


def API_GET_LIST_OF_PRODUCTS(request):
    user_email = request.GET.get('email', '')
    user_password = request.GET.get('password', '')

    if user_email == '' or user_password == '':
        return JsonResponse({"err": "Invalid email or password"}, status=400)
    user = User.objects.get(email=user_email)

    if user is None:
        return JsonResponse({"err": "User not found"}, status=400)

    if not user.check_password(user_password):
        return JsonResponse({"err": "Password is incorrect"}, status=401)

    products_db = Product.objects.exclude(students__id=user.id).order_by('id')
    data = list()
    for product_db in products_db:
        lessons_db = Lesson.objects.filter(product_id=product_db.id).order_by('id')
        product = {
            'id': product_db.id,
            'name': product_db.name,
            'price': product_db.price,
            'lessons_quantity': lessons_db.count(),
            'author_id': product_db.author_id
        }
        data.append(product)
    return JsonResponse(data, safe=False)

def API_GET_LIST_OF_LESSONS(request):
    user_email = request.GET.get('email', '')
    user_password = request.GET.get('password', '')

    if user_email == '' or user_password == '':
        return JsonResponse({"err": "Invalid email or password"}, status=400)
    user = User.objects.get(email=user_email)

    if user is None:
        return JsonResponse({"err": "User not found"}, status=400)

    if not user.check_password(user_password):
        return JsonResponse({"err": "Password is incorrect"}, status=401)

    product_id = request.GET.get('product_id', '')
    products_db = Product.objects.filter(students__id=user.id).order_by('id')

    for product_db in products_db:
        if int(product_db.id) == int(product_id):
            lessons_db = Lesson.objects.filter(product_id=product_id)
            data = list()
            for lesson_db in lessons_db:
                lesson = {
                    'id': lesson_db.id,
                    'name': lesson_db.name,
                    'link_to_video': lesson_db.link_to_video,
                }
                data.append(lesson)
            return JsonResponse(data, safe=False)
    return JsonResponse({"err": "Unauthorized"}, status=400)
