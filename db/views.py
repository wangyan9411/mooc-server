from django.shortcuts import render
import time
import traceback
import MySQLdb.cursors
from models import *
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
import simplejson 
import MySQLdb
import datetime
import base64

@csrf_exempt
def register(request):
    try:

        req = simplejson.loads(request.body)
        print req
        password = req['password']
        email = req['email']
        name = req['name']
        
    
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_user where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            json = {'status' : 'no'}
            response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
            response.set_cookie('name',name,3600)
            print json
            return response
      
        user = User(name = name, email = email, password = password)
        user.save()

        # Toto : check if registered already
        json = {'status':'ok'}
        print json
        response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
        response.set_cookie('name',name,3600)
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def getuserphoto(request):
    print 'r'
    try:
        req = simplejson.loads(request.body)
        
    
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_userphoto";
        cursor.execute(sql)
        result = cursor.fetchall()

        photos = []
        length = len(result)
        for i in range (0, length):
            photos.append(result[i])

        json = {'result':photos}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def getphotobyemail(request):
    print 'r'
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_profile where email = '%s'" % email;
        cursor.execute(sql)
        result = cursor.fetchone()
        
    

        photo = ""
        if result :
            photo = result['imagetext']
        json = {'result':photo}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()


@csrf_exempt
def Forbidden(request):
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        lasttime = req['lasttime']
        print lasttime
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        d1 = datetime.datetime.now()
        d3 = d1 + datetime.timedelta(days=lasttime)
        finish = d3.strftime( '%Y-%m-%d %H:%M:%S')
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_forbiddentime where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            a = ForbiddenTime.objects.get(email = email)
            a.lasttime = finish
            a.starttime = now
            a.save()
        else:
            a = ForbiddenTime(email = email, lasttime = finish, starttime = now)
            a.save() 
        
        json = {'result':'ok'}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def SelectSubject(request):
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        subjectid = req['subjectid']
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_usersubject where email = '%s' and subjectid = '%d'" % (email, subjectid)
        cursor.execute(sql)
        print 'r'
        result = cursor.fetchone()
        if result:
            json = {"result" : "ok"}
            response = HttpResponse(simplejson.dumps(json))
            return response
            
        
        
        if subjectid == 1:
            user = UserSubject(subjectid = subjectid, permission = "teacher", email = email)
            user.save()
        else:
            user = UserSubject(subjectid = subjectid, permission = "student", email = email)
            user.save()

        json = {'result':'ok'}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()
        

@csrf_exempt
def UpdateTimestamp(request):
    try:
        req = simplejson.loads(request.body)
        emailfrom = req['emailfrom']
        emailto = req['emailto']
        timestamp = req['timestamp']
        
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_chatrecord where emailto = '%s'and emailfrom = '%s' and time > '%s' order by time asc" % (emailfrom, emailto, timestamp)
        cursor.execute(sql)
        result = cursor.fetchall()
        length = len(result)
        time = ""
        lastmessage = ""
        if (length > 0):
            lastmessage = result[length-1]["recordtext"] 
            time = result[length-1]["time"]
        print lastmessage
        sql = "select * from db_userstamp where emailfrom = '%s' and emailto = '%s'" % (emailfrom, emailto)
        cursor.execute(sql)
        result = cursor.fetchone()
        print result
        if result:
            a = UserStamp.objects.get(emailfrom = emailfrom , emailto = emailto)
            a.timestamp = timestamp
            a.count = length
            a.time = time
            a.message = lastmessage
            a.save()
        else:
            a = UserStamp(time = time, emailfrom = emailfrom, emailto = emailto, count = length, message = lastmessage, timestamp = timestamp)
            a.save() 
        
        json = {'result':'ok'}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()
@csrf_exempt
def DeleteSubject(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        email = req['email']
        subjectid = req['subjectid']
        
        a = UserSubject.objects.get(email = email , subjectid = subjectid)
        a.delete()

        json = {'result':'ok'}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response

@csrf_exempt
def Post(request):
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        posttitle = req['posttitle']
        posttext = req['posttext']
        subjectid = req['subjectid']
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_forbiddentime where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchone()
        if ( result and result["lasttime"] > now ):
            timef = datetime.datetime.strptime(result["lasttime"], '%Y-%m-%d %H:%M:%S')
            endtime = datetime.datetime.now()
            remaindays = (timef-endtime).days
            remainseconds = (timef-endtime).seconds
            json = {'result':'no', "remaindays" :remaindays, "remainseconds" : remainseconds }
            print json

            response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
            return response

        sql = "select * from db_profile where email = '%s'" % (email);
        cursor.execute(sql)
        photo = cursor.fetchone()
        phototext = ""
        if photo :
            phototext = photo['imagetext']
        
        userpost = UserPost( imagetext = phototext, posttime = now, email = email, posttitle = posttitle, posttext = posttext, subjectid = subjectid)
        userpost.save()


        json = {'result':'yes'}
        print json

        response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def SelectCourse(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        email = req['email']
        subjectid = req['subjectid']
        permission = "student" 
        usersubject = UserSubject(email = email, permission = permission, subjectid = subjectid)
        usersubject.save()


        json = {'result':'ok'}
        print json

        response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
        return response

@csrf_exempt
def UpdateProfile(request):
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        gender = req['gender']
        birthday = req['birthday']
        realname = req['realname']
        region = req['region']
        usertype = "student"
        photoid = req['photoid']
        #now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)


        sql = "select * from db_userphoto where id = '%d'" % (photoid);
        cursor.execute(sql)
        result = cursor.fetchone()

        profile = Profile(imagetext = result['imagetext'], usertype = usertype, email = email, gender = gender, realname = realname, birthday = birthday, region = region)
        profile.save()
        a = UserPost.objects.filter(email = email)
        for i in range ( 0 , len(a)) :
            a[i].imagetext = result['imagetext']
            a[i].save()

        a = PostFloor.objects.filter(email = email)
        for i in range ( 0 , len(a)) :
            a[i].imagetext = result['imagetext']
            a[i].save()

        json = {'result':'ok'}
        print json

        response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def ReplyPost(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        email = req['email']
        postid = req['postid']
        floortext = req['floortext']
        floorresponse = req['floorresponse']
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_profile where email = '%s'" % (email);
        cursor.execute(sql)
        photo = cursor.fetchone()
        phototext = ""
        if photo :
            phototext = photo['imagetext']

        post = PostFloor(imagetext = phototext, email = email, floortime = now, floorresponse = floorresponse, postid = postid, floortext = floortext)
        post.save()

        json = {'result': 'ok'}
        print json

        response = HttpResponse(simplejson.dumps(json))
        # Todo : set the cookie
        return response

@csrf_exempt
def login(request):
    try:
        req = simplejson.loads(request.body)
        passWord = req['password']
        email = req['email']

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        #cursor = db.cursor()
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_user where email = '%s' and password = '%s'" % (email, passWord)
        cursor.execute(sql)
        result = cursor.fetchone()

        if not result:
            status = "no"
        else:
            status = "ok"

        json = {'status':status, 'result' : result}
        print (json)
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()
    
@csrf_exempt
def GetEssence(request):
#    if request.method == 'POST':
    try:
        req = simplejson.loads(request.body)
        subjectid = req["subjectid"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        #cursor = db.cursor()
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_userpost where exist = True and essence = True and subjectid = '%d' order by posttime desc"% (subjectid)
        cursor.execute(sql)
        result = cursor.fetchall()
        final = []

        count = []
        length = len(result)
        for i in range (0, length):
            final.append(result[i])
            postid = result[i]["id"]
            sql = "select * from db_postfloor where postid = '%d'"% (postid)
            cursor.execute(sql)
            res = cursor.fetchall()
            l = len(res)
            count.append(l)

        json = {'result' : final, "floorcount" : count}
        print (json)
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetProfileByEmail(request):
    if request.method == 'POST':
        print "r"
        req = simplejson.loads(request.body)
        email = req['email']

        print "r"
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        #cursor = db.cursor()
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_profile where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchone()

        print "r"
        if not result:
            status = "no"
        else:
            status = "ok"

        json = {'status':status, 'result' : result}
        print (json)
        return HttpResponse(simplejson.dumps(json))
@csrf_exempt
def GetProfileByName(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        email = req['email']

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        #cursor = db.cursor()
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_profile where realname = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchone()

        if not result:
            status = "no"
        else:
            status = "ok"

        json = {'status':status, 'result' : result}
        print (json)
        return HttpResponse(simplejson.dumps(json))
@csrf_exempt
def UserAllSubject(request):
    print "r"
    # get email    return all the subjectname permissions (and info)
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        print req
        email = req['email']
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_usersubject where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchall()
        

        length = len(result)
        subjectnames = []
        for i in range (0, length):
            dictionary = result[i]
            subjectid = dictionary.get("subjectid")
            sql = "select * from db_subjectinfo where subjectid = '%d'" % subjectid
            cursor.execute(sql)
            subjectinfo = cursor.fetchone()
            subjectnames.append(subjectinfo)

        json = {'subjects': subjectnames}
        print (json)
        return HttpResponse(simplejson.dumps(json))
    
@csrf_exempt
def GetPermissions(request):
    # get email    return all the subjectname permissions (and info)
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        email = req['email']
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_usersubject where email = '%s'" % (email)
        cursor.execute(sql)
        result = cursor.fetchall()
        

        length = len(result)
        subjectnames = []
        for i in range (0, length):
            subjectnames.append(result[i])

        json = {'subjects': subjectnames}
        print (json)
        return HttpResponse(simplejson.dumps(json))

@csrf_exempt
def AllSubject(request):
    # get email    return all the subjectname permissions (and info)
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_subjectinfo" 
        cursor.execute(sql)
        result = cursor.fetchall()
        

        length = len(result)
        subjectnames = []
        for i in range (0, length):
            subjectnames.append(result[i])

        json = {'result': subjectnames}
        print (json)
        return HttpResponse(simplejson.dumps(json))

@csrf_exempt
def SubjectAllPost(request):
    #if request.method == 'POST':
    try:
        req = simplejson.loads(request.body)

        subjectid = req["subjectid"]
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_userpost where subjectid = '%d' and exist = True order by toppost desc ,toptime desc, posttime desc"% (subjectid)
        cursor.execute(sql)
        result = cursor.fetchall()

        length = len(result)
        postnames = []
        count = []
        for i in range (0, length):
            postnames.append(result[i])
            postid = result[i]["id"]
            sql = "select * from db_postfloor where postid = '%d'"% (postid)
            cursor.execute(sql)
            res = cursor.fetchall()
            length = len(res)
            count.append(length)

        json = {'result':postnames, "floorcount" : count}
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        print_exc()


@csrf_exempt
def SearchPost(request):
    #if request.method == 'POST':
    try:
        req = simplejson.loads(request.body)

        posttitle = req["posttitle"]
        key = posttitle.split(" ")
	print key
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_userpost where true = true"
        l = len(key)
        for i in range (0, l):
            if key[i] != "":
                sql = sql + " and (posttext like '%s' or posttitle like '%s')" % ("%" + key[i] + "%", "%" + key[i] + "%")

        sql = sql + " and exist = True order by toppost desc ,toptime desc, posttime desc"
        cursor.execute(sql)
        result = cursor.fetchall()

        length = len(result)
        postnames = []
        count = []
        for i in range (0, length):
            postnames.append(result[i])
            postid = result[i]["id"]
            sql = "select * from db_postfloor where postid = '%d'"% (postid)
            cursor.execute(sql)
            res = cursor.fetchall()
            l = len(res)
            count.append(l)

        json = {'result':postnames, "floorcount" : count}
        return HttpResponse(simplejson.dumps(json))
    except:
        print_exc()

@csrf_exempt
def PostAllFloor(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        postid = req['postid']
        

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_postfloor where postid = '%d'"% (postid)
        cursor.execute(sql)
        result = cursor.fetchall()

        length = len(result)
        floor = []
        
        for i in range (0, length):
            floor.append(result[i])
        sql = "select * from db_userpost where id = '%d'"% (postid)
        cursor.execute(sql)
        postres = cursor.fetchone()
        
        json = { "result" : floor, "post" : postres }
        print json
        return HttpResponse(simplejson.dumps(json))

@csrf_exempt
def GetChat(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        req = simplejson.loads(request.body)
        
        emailto = req["emailto"]
        emailfrom = req["emailfrom"]
        timestamp = req["timestamp"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        if (timestamp == "0"):
            sql = "select * from db_chatrecord where (emailto = '%s'and emailfrom = '%s' and time > '%s') or (emailto = '%s' and emailfrom = '%s' and time > '%s' ) order by time asc" % (emailfrom, emailto, timestamp, emailto, emailfrom, timestamp)
        else:
            sql = "select * from db_chatrecord where emailto = '%s'and emailfrom = '%s' and time > '%s' order by time asc" % (emailfrom, emailto, timestamp)
        cursor.execute(sql)
        result = cursor.fetchall()



        length = len(result)
        chatrecord = []
        for i in range (0, length):
            chatrecord.append(result[i])

        json = { "result" : chatrecord }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetChatFrom(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        req = simplejson.loads(request.body)
        
        emailfrom = req["emailfrom"]
        emailto = req["emailto"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_chatrecord where emailfrom = '%s' and emailto = '%s' " % ( emailfrom, emailto)
        cursor.execute(sql)
        result = cursor.fetchall()

        length = len(result)
        chatrecord = []
        for i in range (0, length):
            chatrecord.append(result[i])

        json = { "result" : chatrecord }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def PostChat(request):
    print "r"
    try:
        req = simplejson.loads(request.body)
        emailfrom = req['emailfrom']
        emailto = req['emailto']
        recordtext = req["recordtext"]
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        chatrecord = ChatRecord(emailfrom = emailfrom, emailto = emailto, recordtext = recordtext, time = now)
        chatrecord.save()

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_userstamp where emailfrom = '%s' and emailto = '%s'" % (emailto, emailfrom)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            a = UserStamp.objects.get(emailfrom = emailto , emailto = emailfrom)
            a.count = a.count + 1 
            a.time = now
            a.message = recordtext
            a.save()
        else:
            a = UserStamp(time = now, emailfrom = emailto, emailto = emailfrom, count = 1, message = recordtext)
            a.save() 
        json = {'result':'ok'}
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def GetTimestamp(request):
    print "r"
    #if request.method == 'POST':
    try:
        req = simplejson.loads(request.body)
        emailfrom = req["emailfrom"]
        emailto = req["emailto"]
        
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_chatrecord where emailto = '%s' and emailfrom = '%s' order by time desc"% (emailfrom, emailto)
        cursor.execute(sql)
        result = cursor.fetchall()
        length = len(result)
        if ( length > 0 ):
           now = result[0]["time"]
        else:
           now = "0"
        json = {'result':now }
        response = HttpResponse(simplejson.dumps(json))
        return response
    except:
        traceback.print_exc()

@csrf_exempt
def AddContacts(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        emailfrom = req['emailfrom']
        emailto = req['emailto']
        extratext = req["extratext"]
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailfrom = '%s' and emailto = '%s'"% (emailfrom, emailto)
        cursor.execute(sql)
        result = cursor.fetchall()
        length = len(result)
        if (length == 0 ):
            addcontacts = AddContact(emailfrom = emailfrom, emailto = emailto, extratext = extratext, time = now)
            addcontacts.save()
            json = {'result':'ok'}
        else :
            json = {"result":"no"}
        print json
        response = HttpResponse(simplejson.dumps(json))
        return response

@csrf_exempt
def HaveRead(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        emailto = req["emailto"]
        emailfrom = req["emailfrom"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "update db_chatrecord set isread = True where emailfrom = '%s' and emailto = '%s'" % (emailfrom, emailto)
        cursor.execute(sql)


        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def UpdateContacts(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        req = simplejson.loads(request.body)
        
        et = req["emailto"]
        ef = req["emailfrom"]
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailfrom = '%s' and emailto = '%s'"% (ef, et)
        cursor.execute(sql)
        result = cursor.fetchall()
        length = len(result)
        if (length == 0 ):
            json = { "result" : "ok" }
            return HttpResponse(simplejson.dumps(json))

        print "length ----------------------"
        print length
        a = AddContact.objects.get(emailto = et , emailfrom = ef)
        a.approve = True
        a.save()

        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def RejectContacts(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        et = req["emailto"]
        ef = req["emailfrom"]
        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailfrom = '%s' and emailto = '%s'"% (ef, et)
        cursor.execute(sql)
        result = cursor.fetchall()
        length = len(result)
        if (length == 0 ):
            json = { "result" : "ok" }
            return HttpResponse(simplejson.dumps(json))

        print "length ----------------------"
        print length
        a = AddContact.objects.get(emailto = et , emailfrom = ef)
        a.reject = True
        a.save()
        print "r"


        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def Informed(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        et = req["emailto"]
        ef = req["emailfrom"]

        a = AddContact.objects.get(emailto = et , emailfrom = ef)
        a.doublecheck = True
        a.save()


        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def TopPost(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        

        postid = req["postid"]

        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        a = UserPost.objects.get(id = postid)
        a.toppost = True
        a.toptime = now
        a.save()

        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def EssencePost(request):
    #if request.method == 'POST':
    try:
        print "r"
        req = simplejson.loads(request.body)
        

        pi = req["postid"]

        a = UserPost.objects.get(id = pi)
        a.essence = True
        a.save()


        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def RemovePost(request):
    #if request.method == 'POST':
    try:
        print "r"
        req = simplejson.loads(request.body)
        

        pid = req["postid"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        c = UserPost.objects.get(id = pid)       
        c.exist = False
        c.save()
        #print c
        #sql = "update db_userpost set exist = False where id = '%d'" % (postid)
        #cursor.execute(sql)


        json = { "result" : "ok" }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def SearchByEmail(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        email = req["email"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_user where email = '%s'" % (email)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i])
        json = { "result" : contacts }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetAllUser(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_user"
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i])
        json = { "result" : contacts }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def SearchByName(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        email = req["email"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_profile where realname = '%s'" % (email)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i])
        json = { "result" : contacts }
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def SearchPostByName(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        email = req["email"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_profile where realname = '%s'" % (email)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i]["email"])
        contacts.append(email)
        length = len(contacts)
        posts = []
        for i in range (0,length) :
            sql = "select * from db_userpost where email = '%s'" % (contacts[i])
            cursor.execute(sql)
            result = cursor.fetchall()
            l = len(result)
            for k in range ( 0, l ) :
                posts.append(result[k])

        length = len(posts)
        count = []
        print "r"
        for i in range (0, length):
            postid = posts[i]["id"]
            sql = "select * from db_postfloor where postid = '%d'"% (postid)
            cursor.execute(sql)
            res = cursor.fetchall()
            l = len(res)
            count.append(l)

        json = {'result':posts, "floorcount" : count}
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetUnread(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        req = simplejson.loads(request.body)
        
        emailto = req["email"]
        type_ = req["type"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailto = '%s' and approve = True" % (emailto)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            if (result[i]["emailto"] == emailto) :
                contacts.append(result[i]["emailfrom"])
            else:
                contacts.append(result[i]["emailto"])
        sql = "select * from db_addcontact where emailfrom = '%s' and approve = True" % (emailto)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        for i in range (0, length):
            if (result[i]["emailto"] == emailto) :
                contacts.append(result[i]["emailfrom"])
            else:
                contacts.append(result[i]["emailto"])

        length = len(contacts)
        res = []
        if type_ == "0":
            photos = []
            for i in range (0, length):
                sql = "select * from db_userstamp where emailfrom = '%s' and emailto = '%s'" % (emailto, contacts[i])

                cursor.execute(sql)
                result = cursor.fetchone()
                phototext = ""

                sql = "select * from db_profile where email = '%s'" % (contacts[i]);
                cursor.execute(sql)
                photo = cursor.fetchone()
                phototext = ""
                if photo :
                    phototext = photo['imagetext']
            
                if result:
                    dic = {"imagetext" : phototext, "emailto" : contacts[i], "message" : result["message"], "time" :result['time'], "count" : result['count']}
                    res.append(dic)
                else:
                    dic = {"imagetext" : phototext, "emailto" : contacts[i], "message" : "", "time" : "", "count" : 0}
                    res.append(dic)
        if type_ == "1":
            photos = []
            for i in range (0, length):
                sql = "select * from db_userstamp where emailfrom = '%s' and emailto = '%s'" % (emailto, contacts[i])

                cursor.execute(sql)
                result = cursor.fetchone()
                phototext = ""

                s = '''sql = "select * from db_profile where email = '%s'" % (contacts[i]);
                cursor.execute(sql)
                photo = cursor.fetchone()
                phototext = ""
                if photo :
                    phototext = photo['imagetext']
                '''
                if result:
                    dic = {"imagetext" : phototext, "emailto" : contacts[i], "message" : result["message"], "time" :result['time'], "count" : result['count']}
                    res.append(dic)
                else:
                    dic = {"imagetext" : phototext, "emailto" : contacts[i], "message" : "", "time" : "", "count" : 0}
                    res.append(dic)
        if type_ == "2":
            
            count = 0
            for i in range (0, length):
                sql = "select * from db_userstamp where emailfrom = '%s' and emailto = '%s'" % (emailto, contacts[i])

                cursor.execute(sql)
                result = cursor.fetchone()

                if result:
                    count = count + result["count"]               
            count = str(count)
            res = count
        
       
        json = { "result" : res }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetContacts(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        emailto = req["email"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailto = '%s' and approve = True" % (emailto)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i])
        sql = "select * from db_addcontact where emailfrom = '%s' and approve = True" % (emailto)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        for i in range (0, length):
            contacts.append(result[i])

        json = { "result" : contacts }
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def GetUnsolvedContacts(request):
    #if request.method == 'POST':
    try:
    #    string mm = DateTime.Now.ToString("yyyy-MM-dd-m")
        print "r"
        req = simplejson.loads(request.body)
        
        emailto = req["email"]

        db = MySQLdb.connect("localhost", "root", "", "mooc")
        cursor = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = "select * from db_addcontact where emailto = '%s' and reject = False and approve = False" % (emailto)
        cursor.execute(sql)


        result = cursor.fetchall()

        length = len(result)
        contacts = []
        for i in range (0, length):
            contacts.append(result[i])

        json = { "result" : contacts }
        print json
        return HttpResponse(simplejson.dumps(json))
    except:
        traceback.print_exc()

@csrf_exempt
def test(request):
    try:
        for i in range ( 1, 16):
            str = bytes(i)
            filename = '/home/wangyan/data/' + str
            f=open(filename,'rb')
            ls_f=base64.b64encode(f.read())
            p = UserPhoto(imagetext = ls_f)
            p.save()
            f.close()
        for i in range ( 1, 6):
            a = SubjectInfo.objects.get(subjectid = i)
            print 'r'
            str = bytes(i)
            filename = '/home/wangyan/data/' + str + '.jpg'
            f=open(filename,'rb')
            ls_f=base64.b64encode(f.read())
            a.imagetext = ls_f
            a.save()
            f.close()
        print "recieve"
        html = '''<html>
        <body>

        <h1>My First Heading</h1>

        <p>My first paragraph.</p>

        </body>
        </html>
        '''
        return HttpResponse(html)
    except:
        traceback.print_exc()

