from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse
from django.views import View

from owner.models import Owner, Dog

class OwnersView(View):
    def post(self, request):
        data = json.loads(request.body)
        Owner.objects.create(
            name = data['owner_name'],
            email = data['owner_email'],
            age = data['owner_age']
        )
        return JsonResponse({'MESSAGE':'CREATED'}, status=201)

    def get(self, request):
        owners = Owner.objects.all()
        results = []
        for owner in owners:
            dogs = owner.dog_set.all()
            dog_list = []
            for dog in dogs:
                dog_list.append(
                    {
                        'dog_name':dog.name,
                        'dog_age':dog.age,
                    }
                )
            results.append(                  
                {
                    "name" : owner.name, 
                    "email" : owner.email,
                    "age" : owner.age,
                    "dog_info" : dog_list, 
                }
            )
        return JsonResponse({'result':results}, status=200)

class DogsView(View):
    def post(self, request):
        data = json.loads(request.body)
        Dog.objects.create(
            owner = Owner.objects.get(name=data['owner']),
            name = data['dog_name'],
            age = data['dog_age']
        )
        return JsonResponse({'MESSAGE':'CREATED'}, status=201)

    def get(self, request):
        dogs = Dog.objects.all()
        results = []
         
        for dog in dogs:      
            results.append(
                {   
                    "owner" : dog.owner.name,
                    "name" : dog.name, 
                    "age" : dog.age
                }
            )
        return JsonResponse({'result':results}, status=200)