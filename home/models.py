from django.db import models
import asyncio
import telegram
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from PIL import Image
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название партнера')
    link = models.URLField(max_length=200, verbose_name='Ссылка на партнера')
    logo = models.ImageField(upload_to='partners', help_text='Лого в формате png с размером 200x200')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name} - {self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class TruckType(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name='Название типа грузовика'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип грузовика'
        verbose_name_plural = 'Типы грузовиков'


class Order(models.Model):
    from_where = models.CharField(max_length=500, verbose_name='Откуда')
    to_where = models.CharField(max_length=500, verbose_name='Куда')
    email = models.EmailField(verbose_name='электронная почта', blank=True, null=True)
    weight = models.IntegerField(verbose_name='Вес')
    phone = models.CharField(max_length=30, verbose_name='телефон')
    when = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Когда')
    truck_type = models.ForeignKey(TruckType, on_delete=models.SET_NULL, verbose_name='Тип грузовика', null=True)

    def __str__(self):
        return f'{self.from_where} - {self.to_where}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

# Signal receiver function
@receiver(post_save, sender=Order)
def post_order_on_telegram(sender, instance, created, **kwargs):
    if created:
        asyncio.run(post_event_on_telegram(instance.from_where,instance.phone,instance.email,instance.to_where,  instance.weight, instance.when, instance.truck_type))

async def post_event_on_telegram(from_where,phone, to_where, email, weight, when, truck_type):
    event = {
        'from_where': from_where,
        'phone': phone,
        'email' : email ,
        'to_where': to_where,
        'weight': weight,
        'when': when,
        'truck_type': truck_type
    }
    message_html = render_to_string('event.html', {'event': event})
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    await bot.send_message(chat_id="@%s" % telegram_settings['channel_name'], text=message_html, parse_mode='HTML')
    print('event sent')



class Blog(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=300, verbose_name='Заголовок'),
    )
    image = models.ImageField(upload_to='blogs', verbose_name='Изображение')

    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #     new_size = (857, 539)
    #     img.thumbnail(new_size)
    #     img.save(self.image.path)
        
    #     super().save(*args, **kwargs)
    #aaskdugvasl

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'




