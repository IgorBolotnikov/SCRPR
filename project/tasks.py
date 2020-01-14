from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab

from .models import SoldGoods
from .parser import PizzaParser


logger = get_task_logger(__name__)


@task(name='create_order')
def create_order(cart_items, order_id):
    goods = [SoldGoods(
        goods_name_id=int(key),
        amount=value['quantity'],
        order_id=order_id
    ) for key, value in cart_items.items()]
    SoldGoods.objects.bulk_create(goods)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="parse_pizzas",
    ignore_result=True
)
def parse_pizzas():
    PizzaParser().parse_page()
