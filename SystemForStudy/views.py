from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from SystemForStudy.models import Product, Lesson


class GetProductsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        if request.method == 'GET':
            if request.user.is_authenticated:
                products_db = Product.objects.exclude(students__id=request.user.id).order_by('id')
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
        return JsonResponse({"msg": "Incorrect request"}, status=404)


class GetLessonsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        if request.method == 'GET':
            product_id = request.GET.get('product_id', '')
            products_db = Product.objects.filter(students__id=request.user.id).order_by('id')

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
            return JsonResponse({"msg": "Unauthorized"}, status=400)


class GetQuantityOfStudentsAPIView(APIView):
    @staticmethod
    def get(request):
        if request.method == 'GET':
            product_id = request.GET.get('product_id', '')
            if product_id == '':
                return JsonResponse({"msg": "Product id is incorrect"}, status=404)

            product_db = Product.objects.get(id=product_id)
            if product_db is None:
                return JsonResponse({"msg": "Not found"}, status=404)

            quantity_of_students = product_db.students.count()
            return JsonResponse({"quantity_of_students": quantity_of_students}, status=200)


class RegisterStudentAPIView(APIView):
    @staticmethod
    def post(request):
        if request.method == "POST":
            product_id = request.POST.get('product_id', '')
            product = Product.objects.get(id=int(product_id))
            product.students.add(request.user)
            product.rebuild_groups()
            product.save()
            return JsonResponse({"msg": "Student registered"}, status=200)
