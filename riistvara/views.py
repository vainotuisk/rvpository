from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
import pyrebase
import datetime
#TODO koodilugemisest: https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/
config = {
    "apiKey": "AIzaSyBCmCIIxZ7pVEdQWvdM8WxmQv5LPb8yZak",
    "authDomain": "scorching-inferno-1325.firebaseapp.com",
    "databaseURL": "https://scorching-inferno-1325.firebaseio.com",
    "projectId": "scorching-inferno-1325",
    "storageBucket": "",
#    "serviceAccount": "rvpository-7b59e0c3deda.json",
    "messagingSenderId": "333374404394"
}

# initialize app with config
firebase = pyrebase.initialize_app(config)

# authenticate a user
authe = firebase.auth()
#user = auth.sign_in_with_email_and_password("vainotuisk@gmail.com", "12T00likest")



db = firebase.database()

email = " "

def index(request):
    return HttpResponse("Halloo, alguslehe index siin.")
def ruumid(request):
    return HttpResponse("Halloo, ruumid index siin.")


def get_users(request):
    users = db.child("users").get()
    return render(request, 'users.html', {'users': users.val()})
def signin(request):
    return render(request,"signin.html")

def postsign(request):
    global email
    email=request.POST.get('e-post')
    passw=request.POST.get('salakas')
    print("EEpost: "+str(email))
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message = 'vigased andmed'
        return render(request, "signin.html",{"msg":message})
    print(user['idToken'])
    sessionId= user['idToken']
    request.session['uid']=str(sessionId)
    return render(request,'avaleht.html',{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'signin.html')

def uusruum(request):
    print('e-post: ' + str(email))
    return render(request,'create_ruum.html',{"e":email})
def postruum(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Europe/Tallinn')
    time_now=datetime.now(timezone.utc).astimezone(tz).strftime('%d.%m.%Y %H:%M')
    ruumikood = request.POST.get('ruumikood')
    ruumikirjeldus = request.POST.get('ruumikirjeldus')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    email=a['email']
    a = a['localId']
    data = {
        "ruumikood":ruumikood,
        "ruumikirjeldus": ruumikirjeldus,
        "muutja":email,
        "timestamp":str(time_now)
    }

    db.child('ruumid').child(ruumikood).set(data)
    return render(request,'avaleht.html',{"e":email})
def listruum(request):
    ruumikoodid = db.child("ruumid").shallow().get().val()
    ruumikoodide_list= []
    for i in ruumikoodid:
        ruumikoodide_list.append(i)
        ruumikoodide_list.sort()
    kirjeldused=[]
    for i in ruumikoodide_list:
        kirjeldus= db.child("ruumid").child(i).child("ruumikirjeldus").get().val()
        kirjeldused.append(kirjeldus)
    print(ruumikoodid)
    print(ruumikoodide_list)
    print(kirjeldused)
    ajad=[]
    for i in ruumikoodide_list:
        aeg=db.child("ruumid").child(i).child("timestamp").get().val()
        ajad.append(aeg)
    print("========")
    print(ajad)
    # ilusad_ajad=[]
    # for i in ajad:
    #
    #     aeg=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d.%m.%Y')
    #     ilusad_ajad.append(aeg)
    ruumideandmed=zip(ruumikoodide_list,kirjeldused,ajad)
    print(ruumideandmed)
    return render(request,'listruum.html',{"ruumid":ruumideandmed})
def uusasi(request):
    kirjeldused = []
    ruumikoodide_list = []
    ruumikoodid = db.child("ruumid").shallow().get().val()
    for i in ruumikoodid:
        ruumikoodide_list.append(i)
        ruumikoodide_list.sort()
    for i in ruumikoodide_list:
        kirjeldus = db.child("ruumid").child(i).child("ruumikirjeldus").get().val()
        kirjeldused.append(kirjeldus)
    ruumideandmed = zip(ruumikoodide_list, kirjeldused)
    return render(request,'create_asi.html',{"ruumid":ruumideandmed})
def ruumdetails(request):
    ruumikood = request.GET.get('k')
    ruumikirjeldus= db.child("ruumid").child(ruumikood).child("ruumikirjeldus").get().val()
    muutja=db.child("ruumid").child(ruumikood).child("muutja").get().val()
    aeg=db.child("ruumid").child(ruumikood).child("timestamp").get().val()
    return render(request,'ruumdetails.html',{"ruumikood":ruumikood,"aeg":aeg,"muutja":muutja,"ruumikirjeldus":ruumikirjeldus})
def ruumedit(request):
    ruumikood = request.GET.get('k')
    ruumikirjeldus = db.child("ruumid").child(ruumikood).child("ruumikirjeldus").get().val()
    muutja = db.child("ruumid").child(ruumikood).child("muutja").get().val()
    aeg = db.child("ruumid").child(ruumikood).child("timestamp").get().val()
    return render(request,'ruumedit.html',{"ruumikood":ruumikood,"aeg":aeg,"muutja":muutja,"ruumikirjeldus":ruumikirjeldus})
def ruumdel(request):
    ruumikood = request.GET.get('k')
    return render(request,'ruumdel.html',{"ruumikood":ruumikood})
def postasi(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Europe/Tallinn')
    time_now=datetime.now(timezone.utc).astimezone(tz).strftime('%d.%m.%Y %H:%M')
    asjakood = request.POST.get('asjakood')
    asjakirjeldus = request.POST.get('asjakirjeldus')
    asjaruum = request.POST.get('asjaruum')
    asjatyyp = request.POST.get('asjatyyp')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    email=a['email']
    a = a['localId']
    data = {
        "asjatyyp":asjatyyp,
        "asjakirjeldus": asjakirjeldus,
        "muutja":email,
        "asjaruum":asjaruum,
        "timestamp":str(time_now)
    }

    db.child('asjad').child(asjakood).set(data)
    return render(request,'avaleht.html',{"e":email})
def listasi(request):
    asjakoodid = db.child("asjad").shallow().get().val()
    asjakoodide_list= []
    for i in asjakoodid:
        asjakoodide_list.append(i)
        asjakoodide_list.sort()
    print(asjakoodide_list)
    kirjeldused=[]
    for i in asjakoodide_list:
        kirjeldus= db.child("asjad").child(i).child("asjakirjeldus").get().val()
        kirjeldused.append(kirjeldus)
    ajad=[]
    for i in asjakoodide_list:
        aeg=db.child("asjad").child(i).child("timestamp").get().val()
        ajad.append(aeg)
    print("========")
    print(ajad)
    ruumid=[]
    for i in asjakoodide_list:
        ruum=db.child("asjad").child(i).child("asjaruum").get().val()
        print(ruum)
        ruumid.append(ruum)
    asjadeandmed=zip(asjakoodide_list,kirjeldused,ajad,ruumid)
    print(asjadeandmed)
    print(kirjeldused)
    print(ruumid)
    return render(request,'listasi.html',{"asjad":asjadeandmed})
def asiedit(request):
    ruumikood = request.GET.get('k')
    ruumikirjeldus = db.child("ruumid").child(ruumikood).child("ruumikirjeldus").get().val()
    muutja = db.child("ruumid").child(ruumikood).child("muutja").get().val()
    aeg = db.child("ruumid").child(ruumikood).child("timestamp").get().val()
    return render(request,'asiedit.html',{"ruumikood":ruumikood,"aeg":aeg,"muutja":muutja,"ruumikirjeldus":ruumikirjeldus})
def asidetails(request):
    kood = request.GET.get('k')
    kirjeldus= db.child("asjad").child(kood).child("asjakirjeldus").get().val()
    print(kirjeldus)
    muutja=db.child("asjad").child(kood).child("muutja").get().val()
    aeg=db.child("asjad").child(kood).child("timestamp").get().val()
    try:
        lookoodid=db.child("asjad").child(kood).child("ajalugu").shallow().get().val()
        lookoodidelist = []
        for i in lookoodid:
            lookoodidelist.append(i)
        lookirjeldused = []
        for i in lookoodidelist:
            lookirjeldus = db.child("asjad").child(kood).child("ajalugu").child(i).child("kirjeldus").get().val()
            lookirjeldused.append(lookirjeldus)
        loolisajad = []
        for i in lookoodid:
            loolisaja = db.child("asjad").child(kood).child("ajalugu").child(i).child("muutja").get().val()
            loolisajad.append(loolisaja)
        looajad = []
        for i in lookoodid:
            looaeg = db.child("asjad").child(kood).child("ajalugu").child(i).child("timestamp").get().val()
            looajad.append(looaeg)

        print("Lugude kirjelduste massiiv::: " + str(lookirjeldused))
        asjalood = zip(loolisajad, lookirjeldused, looajad)
        return render(request, 'asidetails.html',
                      {"kood": kood, "aeg": aeg, "muutja": muutja, "kirjeldus": kirjeldus, "ajalugu": asjalood})
    except:
        return render(request, 'asidetails.html', {"kood": kood, "aeg": aeg, "muutja": muutja, "kirjeldus": kirjeldus})

def postlugu(request):
    kood = request.POST.get('kood')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    email = a['email']
    lugu=request.POST.get("lugu")
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Europe/Tallinn')
    time_now = datetime.now(timezone.utc).astimezone(tz).strftime('%d.%m.%Y %H:%M')
    aeg=str(time_now)
    data= {
        "muutja":email,
        "kirjeldus":lugu,
        "timestamp":aeg
    }
    db.child('asjad').child(kood).child("ajalugu").push(data)
    return render(request, 'asidetails.html', {"kood": kood, "aeg": aeg, "muutja": email, "kirjeldus": lugu})
def lisalugu(request):
    ese=request.GET.get('k')
    return render(request,'create_lugu.html',{"asi":ese})
