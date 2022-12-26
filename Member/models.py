from django.db import models

class School(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=45)
    tel = models.CharField(db_column='tel', max_length=45)
    address = models.CharField(db_column='address', max_length=45)
    website = models.CharField(db_column='website', max_length=45)
    image = models.ImageField(db_column='image',upload_to='school_img/', blank=False, null=False)
    public_private = models.CharField(db_column='public/private', max_length=45)
    union = models.CharField(db_column='union', max_length=45)
    school_system = models.CharField(db_column='school_system', max_length=45)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'school'
        managed=False


class Member(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=45)
    identity = models.CharField(db_column='identity', max_length=45)
    sex = models.CharField(db_column='sex', max_length=45)
    birthday = models.DateField(db_column='birthday')
    tel = models.CharField(db_column='tel', max_length=45)
    email = models.EmailField(db_column='email', max_length=45)
    password = models.CharField(db_column='password', max_length=45)
    image = models.ImageField(db_column='image',upload_to='member_pictures/', blank=False, null=False)
    school_id = models.ForeignKey('School', db_column='school_id', on_delete=models.CASCADE)

    #upload_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'member'
        managed=False
