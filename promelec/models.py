from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from core.models import TimestampsMixin


class SitemapURL(TimestampsMixin):
    url = models.URLField(_("URL"), unique=True)

    class Meta:
        verbose_name = 'URL карты сайта'
        verbose_name_plural = 'URL карты сайта'

    def __str__(self):
        return self.url


class PromelecCategory(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        unique_together = ('name', 'parent')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class PromelecBrand(TimestampsMixin):
    name = models.CharField(_("Наименование"), max_length=255, unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class PromelecProduct(TimestampsMixin):
    category = models.ForeignKey(PromelecCategory, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    part_number = models.CharField(_("Партномер"), max_length=255)
    brand = models.ForeignKey(PromelecBrand, on_delete=models.CASCADE, related_name='products', verbose_name='Производитель')
    product_code = models.CharField(_("Код товара"), max_length=20, unique=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.part_number} ({self.brand})"


class PromelecInventory(TimestampsMixin):
    product = models.ForeignKey(PromelecProduct, on_delete=models.CASCADE, related_name='prices', verbose_name='Товар')
    updated_date = models.DateTimeField(_("Дата обновления"))
    data = models.JSONField(_("Данные"), default=dict)

    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризация'

    def __str__(self):
        return f"{self.product} ({self.created_at})"


class StateOder(models.TextChoices):
    SOLD_VERIFICATION = 'SOLD_VERIFICATION', _('Проверка продажи')
    SOLD = 'SOLD', _('Продан')
    RETURNED = 'RETURNED', _('Возвращен')
    RESTOCK_VERIFICATION = 'RESTOCK_VERIFICATION', _('Проверка пополнения')
    RESTOCKED = 'RESTOCKED', _('Пополнен')


class PromelecOrder(TimestampsMixin):
    product = models.ForeignKey(PromelecProduct, on_delete=models.CASCADE, related_name='orders', verbose_name='Товар')
    quantity = models.PositiveIntegerField(_("Количество"))
    warehouse = models.CharField(_("Склад"), max_length=255)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    state = models.CharField(_("Статус"), max_length=20, choices=StateOder.choices, default=StateOder.SOLD_VERIFICATION)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.product} ({self.quantity}) - {self.get_state_display()}"