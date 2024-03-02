from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from SystemForStudy.models import Product, Lesson, Group


class ProductsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
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

    @staticmethod
    def post(request):
        product_name = request.POST.get('product_name', '')
        product_start_time = request.POST.get('product_start_time', '')
        product_price = request.POST.get('product_price', '')
        product_author_id = request.POST.get('product_author_id', '')
        if product_name == '' or product_start_time == '' or product_price == '' or product_author_id == '':
            return JsonResponse({"msg": "Incorrect request"}, status=404)
        author = User.objects.get(id=product_author_id)
        if author is None:
            return JsonResponse({"msg": "Incorrect author id"}, status=404)
        Product.objects.create(name=product_name, start_time=product_start_time,
                               price=product_price, author_id=product_author_id)
        return JsonResponse({"msg": "Product created"}, status=201)


class GetLessonsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        product_id = request.GET.get('product_id', '')
        if product_id == '':
            return JsonResponse({"msg": "Product id is incorrect"}, status=404)

        products_db = Product.objects.filter(students__id=request.user.id).order_by('id')
        if products_db is None:
            return JsonResponse({"msg": "Not found"}, status=404)

        id_found = False
        for product_db in products_db:
            if int(product_db.id) == int(product_id):
                id_found = True
                break
        if id_found:
            lessons_db = Lesson.objects.filter(product_id=product_id)
            if lessons_db is None:
                return JsonResponse({"msg": "No lessons found"}, status=404)

            data = list()
            for lesson_db in lessons_db:
                lesson = {
                    'id': lesson_db.id,
                    'name': lesson_db.name,
                    'link_to_video': lesson_db.link_to_video,
                }
                data.append(lesson)
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"msg": "No id found"}, status=404)


class GetQuantityOfStudentsAPIView(APIView):
    @staticmethod
    def get(request):
        product_id = request.GET.get('product_id', '')
        if product_id == '':
            return JsonResponse({"msg": "Product id is incorrect"}, status=404)

        product_db = Product.objects.get(id=product_id)
        if product_db is None:
            return JsonResponse({"msg": "Not found"}, status=404)

        quantity_of_students = product_db.students.count()
        return JsonResponse({"quantity_of_students": quantity_of_students}, status=200)


class GetPercentOfFullnessPerGroupAPIView(APIView):

    @staticmethod
    def get(request):
        product_id = request.GET.get('product_id', '')
        if product_id == '':
            return JsonResponse({"msg": "Product id is incorrect"}, status=404)

        groups = Group.objects.filter(product_id=product_id).order_by('id')
        if groups is None:
            return JsonResponse({"msg": "Not found"}, status=404)

        data = list()
        for group in groups:
            group_percent_of_fullness = {
                'id': group.id,
                'name': group.name,
                'percent_of_fullness': group.percent_of_fullness()
            }
            data.append(group_percent_of_fullness)
        return JsonResponse(data, safe=False)


class GetProductBuyingRatingAPIView(APIView):

    @staticmethod
    def get(request):
        products = Product.objects.all()
        data = list()
        for product in products:
            product_rating = {
                'id': product.id,
                'name': product.name,
                'author': product.author_id,
                'price': product.price,
                'product_buying_rating': product.buying_rating()
            }
            data.append(product_rating)
        return JsonResponse(data, safe=False)


class StudentAPIView(APIView):

    @staticmethod
    def post(request):
        product_id = request.POST.get('product_id', '')
        if product_id == '':
            return JsonResponse({"msg": "Product id is incorrect"}, status=404)

        product_db = Product.objects.get(id=int(product_id))
        if product_db is None:
            return JsonResponse({"msg": "Not found"}, status=404)

        if product_db.percent_of_fullness() != 100:
            product_db.students.add(request.user)
            product_db.rebuild_groups(user=request.user)
            product_db.save()
            return JsonResponse({"msg": "Student registered"}, status=200)
        else:
            return JsonResponse({"msg": "Failed to register user. Project is full."}, status=404)

    @staticmethod
    def delete(request):
        product_id = request.DELETE.get('product_id', '')
        if product_id == '':
            return JsonResponse({"msg": "Product id is incorrect"}, status=404)

        product_db = Product.objects.get(id=int(product_id))
        if product_db is None:
            return JsonResponse({"msg": "Not Found"}, status=404)

        product_db.students.remove(request.user)
        product_db.save()
        return JsonResponse({"msg": "Student removed successfully"}, status=200)
