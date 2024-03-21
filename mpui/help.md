# Main source (console.urls.py)
```
path('downthreat',views.downthreat,name = 'downthreat')
```
in this the 'home' means localhost (slash) downthreat for that route will execute the function home in the file views.py
# Function routing in (console.views.py)
```
def downthreat(request):
    full_path = '/home/ak/projects/major_project/pipe/threats/threat.csv'
    response = HttpResponse(open(full_path, 'rb').read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=threat.csv'
    return response
```
this is the download module, so when it is called in the html as ```href = downthreat``` then it is sent to urls.py and then forwaded with the request to this function which will handle it. This code downloads the file in the specified location

### Note 
There are several GET POST requests which just differentiate the different types of requests this function can handle

# soul.py
this is your main inference engine, which will start a tcdump for any specified time, which i have chosen as 30 seconds and will be run 4 times, so 2 minutes, every 30 seconds a .pcap file is generated from which we generate flows and save it into another folder with .csv, then this .csv is imported, processed (shaping the data to match the training data for accurate inference). After we have that data, run predict on the saved model, if we detect an anomaly, go to dict on that index save the file, and then append to the threat.csv and send a notification along with it.

# Responsibilty
You can say you did the frontend, created the paths, the filing system for the live feed without any conccurency or data loss and the logging for later inspection. So that includes everything in the templated folder the html files, with all the href calls in the buttons and the tags.
 
I will say i worked on the soul.py, pipelining the data, preparing model,shaping the data, running prediction, threat report generation and some other backend alerting systems.


