from django.db import models
from Member.models import School

class Department(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=45)
    address = models.CharField(db_column='address', max_length=45)
    email = models.CharField(db_column='email', max_length=45)
    manager = models.CharField(db_column='manager', max_length=45)
    tel = models.CharField(db_column='tel',max_length=45)  
    school_id = models.ForeignKey(School, db_column='school_id', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.address
    class Meta:
        db_table = 'department'
