from django.db import models

class User(models.Model):
    email = models.EmailField(primary_key = True)
    name = models.CharField(max_length = 20)
    password = models.CharField(max_length = 30)
    supermonitor = models.BooleanField(default = False)

    def __str__(self):
        return '%s %s %s' % (self.email, self.name, self.password)



class ForbiddenTime(models.Model):
    email = models.EmailField(null = True)
    starttime = models.CharField(max_length = 30)
    lasttime = models.CharField(max_length = 30, default = "0")
    def __str__(self):
        return "" 

class UserSubject(models.Model):
    email = models.EmailField(null = True)
    subjectid = models.IntegerField(blank = True, null = True)
    permission = models.CharField(max_length = 30)
    def __str__(self):
        return '%s %s %s' % (self.email, self.subject, "")

class UserStamp(models.Model):
    emailfrom = models.EmailField(null = True)
    emailto = models.EmailField(null = True)
    timestamp = models.CharField(max_length = 30)
    time = models.CharField(max_length = 30)
    count = models.IntegerField()
    message = models.TextField()
    def __str__(self):
        return '%s %s %s' % (self.emailfrom, self.emailto, "")
'''
class UserAllSubject(models.Model):
    subjectid = models.IntegerField(primary_key = True)
    permission = models.CharField(max_length = 30)
    email = models.EmailField()

    def __str__(self):
        return '%s %s %s' % (self.email, self.subject, "")
'''

class UserPost(models.Model):
    subjectid = models.IntegerField(blank = True, null = True)
    email = models.EmailField()
    posttitle = models.CharField(max_length = 100)
    posttext = models.TextField()
    posttime = models.CharField(null = True, max_length = 40)
    exist = models.BooleanField(default = True)
    essence = models.BooleanField(default = False)
    toppost = models.BooleanField(default = False)
    toptime = models.CharField(null = True, max_length = 40)
    imagetext = models.TextField()
    
    def __str__(self):
        return '%s' % (self.posttext)

class UserPhoto(models.Model):
    imagetext = models.TextField()
    
    def __str__(self):
        return "" 
class SubjectInfo(models.Model):
    subject = models.CharField(max_length = 30)
    subjectid = models.IntegerField (primary_key = True)
    subjectinfo = models.TextField()
    belongto = models.IntegerField()
    teacher = models.CharField(max_length = 30)
    assistant = models.CharField(max_length = 30)
    teacheremail = models.CharField(max_length = 38)
    teacherphone = models.CharField(max_length = 30)
    imagetext = models.TextField()

    def __str__(self):
        return ''

class Profile(models.Model):
    realname = models.CharField(max_length = 30)
    birthday = models.CharField(max_length = 30)
    email = models.EmailField (primary_key = True)
    gender = models.CharField(max_length = 30)
    region = models.CharField(max_length = 30)
    usertype = models.CharField(max_length = 30)
    image= models.ImageField(upload_to='photos/%Y/%m/%d', blank=True,null=True)
    imagetext = models.TextField()
    
    def __str__(self):
        return ''

class PostFloor(models.Model):
    postid = models.IntegerField (blank=True, null=True)
    email = models.EmailField()
    imagetext = models.TextField()
    floorresponse = models.IntegerField()
    floortime = models.CharField(max_length = 30)
    floortext = models.TextField()
    
    def __str__(self):
        return '%s' % (self.posttext)
    
    
class ChatRecord(models.Model):
    emailfrom = models.EmailField()
    emailto = models.EmailField()
    recordtext = models.TextField()
    time = models.CharField(max_length = 40)
    isread = models.BooleanField(default = False)
    def __str__(self):
        return '%s' % (self.posttext)


class AddContact(models.Model):
    emailfrom = models.EmailField()
    emailto = models.EmailField()
    extratext = models.TextField()
    time = models.CharField(max_length = 40)
    approve = models.BooleanField(default = False)
    reject = models.BooleanField(default = False)
    doublecheck = models.BooleanField(default = False)
    def __str__(self):
        return '%s' % (self.posttext)

