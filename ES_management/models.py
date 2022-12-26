from django.db import models
from Member_management.models import Department

class Site(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=45)
    usage = models.CharField(db_column='usage', max_length=45)
    price = models.IntegerField(db_column='price')
    rule = models.CharField(db_column='rule',max_length=200)
    image = models.ImageField(db_column='image', upload_to='site_pictures/')
    address = models.CharField(db_column='address', max_length=45)
    location = models.CharField(db_column='location', max_length=45)
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'site'

class Duration(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    date= models.DateField(db_column='date')
    start = models.IntegerField(db_column='start')
    end = models.IntegerField(db_column='end')
    rent_status = models.IntegerField(db_column='rent_status')
    site_id= models.ForeignKey('Site', db_column='site_id', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'duration'

class Equipment(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=45)
    usage = models.CharField(db_column='usage', max_length=10)
    number = models.IntegerField(db_column='number')
    price = models.IntegerField(db_column='price')
    rule = models.CharField(db_column='rule',max_length=200)
    image = models.ImageField(db_column='image', upload_to='equipment_pictures/')
    department_id= models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'equipment'