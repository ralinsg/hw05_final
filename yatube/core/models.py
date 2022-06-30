from django.db import models


class CreatedModel(models.Model):
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        abstract = True
        ordering = ["-pub_date"]
