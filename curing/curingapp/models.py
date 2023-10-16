from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Project_Master(models.Model):
    Project_ID = models.AutoField(primary_key=True)
    Project_Name = models.CharField(max_length=100)
           
    def __str__(self):
        return self.Project_Name

class Site_Master(models.Model):
    Site_ID = models.AutoField(primary_key=True)
    Site_Name = models.CharField(max_length=100)
    Project = models.ForeignKey(Project_Master, on_delete=models.CASCADE)

    def __str__(self):
        return self.Site_Name


class CustomUser(AbstractUser):
     User_ID = models.AutoField(primary_key=True)
     username = models.CharField(max_length=100,unique=True)
     email=models.CharField(max_length=50)
     Contact_no= models.CharField(max_length=15)
     Project=models.ForeignKey(Project_Master, on_delete=models.CASCADE)
     Site=models.ForeignKey(Site_Master, on_delete=models.CASCADE)
     is_user = models.BooleanField(default=False)
     is_Administrator = models.BooleanField(default=False)

     def __str__(self):
        return self.username

class Structural_Element(models.Model):
    Structural_Element_ID = models.AutoField(primary_key=True)
    Structural_Element = models.CharField(max_length=100)
    No_Of_Days=models.IntegerField()
    Frequency=models.IntegerField()
    Time_Bet_TwoCuring=models.IntegerField(null=True,blank=True)    
    def __str__(self):
        return self.Structural_Element

class Transaction_Concreting(models.Model):
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Transaction_Concreting_ID=models.AutoField(primary_key=True)
    Project = models.ForeignKey(Project_Master,on_delete=models.CASCADE)
    Site = models.ForeignKey(Site_Master,on_delete=models.CASCADE)
    Structural_Element=models.ForeignKey(Structural_Element,on_delete=models.CASCADE)
    Schedule_Date_and_Time=models.DateTimeField()

    def __str__(self):
        return f"Transaction Concreting ID: {self.Transaction_Concreting_ID}"

class Schedule_Curing(models.Model):
    APPROVE_CHOICES = [
        ('Approve', 'Approve'),
        ('Not Approve', 'Not Approve'),
    ]

    Schedule_Curing_ID = models.AutoField(primary_key=True)
    Transaction_Concreting= models.ForeignKey(Transaction_Concreting, on_delete=models.CASCADE)
    Project = models.ForeignKey(Project_Master, on_delete=models.CASCADE)
    Site = models.ForeignKey(Site_Master, on_delete=models.CASCADE)
    Structural_Element = models.ForeignKey(Structural_Element, on_delete=models.CASCADE)
    Schedule_Date_and_Time = models.DateTimeField()
    Image_Of_Curing = models.ImageField(upload_to='curing_images/',null=True,blank=True)
    Status = models.CharField(max_length=11, choices=APPROVE_CHOICES, null=True,blank=True)

    def __str__(self):
        return f'Schedule Curing - {self.Schedule_Curing_ID}'
    
class Curing_Image_Files(models.Model):
    Curing_File_ID=models.AutoField(primary_key=True)
    Curing_File_Name=models.CharField(max_length=100)
    Project=models.ForeignKey(Project_Master,on_delete=models.CASCADE)
    Site=models.ForeignKey(Site_Master,on_delete=models.CASCADE)
    Structural_Element=models.ForeignKey(Structural_Element,on_delete=models.CASCADE)
    Transaction_Concreting=models.ForeignKey(Transaction_Concreting,on_delete=models.CASCADE)
    Schedule_Curing=models.ForeignKey(Schedule_Curing,on_delete=models.CASCADE)

    def __str__(self) :
        return f'Curing_Image_Files - {self.Curing_File_Name}'