import datetime
import random
from django.core.management.base import BaseCommand
from core.models import DishOriginCategory,Dish,VegginessCategory,SpicynessCategory,StartersOrMaincourseCategory


dishOriginCategory = [
    'Indian','Continental','South Indian','Mexican','Italian'
]
spicynessCategory = [
    'less','medium','high'
]

vegginessCategory = [
    'veg','non-veg','vegan'
]
startersOrMaincourseCategory = [
    'starters','main-course'
]

def generate_dishOriginCategory():
    index = random.randint(0, 4)
    return dishOriginCategory[index]


def generate_spicynessCategory():
    index = random.randint(0, 2)
    return spicynessCategory[index]


def generate_vegginessCategory():
    index = random.randint(0, 2)
    return vegginessCategory[index]


def generate_startersOrMaincourseCategory():
    index = random.randint(0, 1)
    return startersOrMaincourseCategory[index]


def generate_price():
    return random.randint(100,500)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='Names of different dishes')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                name = row
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                dishOriginCategory = generate_dishOriginCategory()
                spicynessCategory = generate_spicynessCategory()
                vegginessCategory = generate_vegginessCategory()
                startersOrMaincourseCategory = generate_startersOrMaincourseCategory()
                price = generate_price()
                dishOriginCategorymodel = DishOriginCategory.objects.get_or_create(name=dishOriginCategory)
                spicynessCategorymodel = SpicynessCategory.objects.get_or_create(name=spicynessCategory)
                vegginessCategorymodel = VegginessCategory.objects.get_or_create(name=vegginessCategory)
                startersOrMaincourseCategorymodel = StartersOrMaincourseCategory.objects.get_or_create(name=startersOrMaincourseCategory)


                dish = Dish(
                    name = name,
                    price = price,
                    dishOrigin = DishOriginCategory.objects.get(name = dishOriginCategory),
                    spicyness = SpicynessCategory.objects.get(name = spicynessCategory),
                    vegginess = VegginessCategory.objects.get(name = vegginessCategory),
                    startersOrMaincourse = StartersOrMaincourseCategory.objects.get(name = startersOrMaincourseCategory)
                )

                dish.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
