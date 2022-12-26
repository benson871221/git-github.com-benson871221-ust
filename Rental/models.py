from django.db import models
from Member.models import Member
from ES_management.models import Duration, Equipment

class Rent_Site(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    date = models.DateField(db_column='date')
    status = models.IntegerField(db_column='status')
    timestamp = models.DateTimeField(db_column='timestamp', max_length=45)
    member_id= models.ForeignKey(Member, db_column='member_id', on_delete=models.CASCADE)
    duration_id= models.ForeignKey(Duration, db_column='duration_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'rent_site'

class Rent_Equipment(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    date = models.DateField(db_column='date')
    number = models.IntegerField(db_column='number')
    status = models.IntegerField(db_column='status')
    timestamp = models.DateTimeField(db_column='timestamp')
    member_id= models.ForeignKey(Member, db_column='member_id', on_delete=models.CASCADE)
    equipment_id= models.ForeignKey(Equipment, db_column='equipment_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'rent_equipment'