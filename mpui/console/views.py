from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.core.files.storage import FileSystemStorage
from .soul import main, main2
#from plyer import notification

@csrf_exempt
def home(request):
    if request.method == 'POST':
        for i in range(4):
            main(i)
        return render(request,'index.html')
    else:
        return render(request,'index.html')

def downthreat(request):
        full_path = '/home/ak/projects/major_project/pipe/threats/threat.csv'
        response = HttpResponse(open(full_path, 'rb').read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=threat.csv'
        #notification.notify(
        #title = "Threat Alert",
        #message = f"10 Threats have been detected",
        #timeout = 3
        #)
        return response
        

def upload(request):

    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        uploaded_file.name = 'curr'
        fs.save(uploaded_file.name,uploaded_file)
        return render(request, 'upload.html',{'success':'Successfully Uploaded'})      
    else:
        return render(request, 'upload.html')
    
def pcap(request):
    main2()
    full_path = '/home/ak/projects/major_project/pipe/threats2/threat.csv'
    response = HttpResponse(open(full_path, 'rb').read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=threat_pcap.csv'
    return response
    
    