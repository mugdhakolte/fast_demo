from tortoise import fields, models


class TextSummery(models.Model):
    url = fields.TextField()
    summery = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url
