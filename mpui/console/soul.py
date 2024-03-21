import os
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from plyer import notification
import time
#from pydub.playback import play
#from pydub import AudioSegment

def cic(a):
    os.system(f"cicflowmeter -f /home/ak/projects/major_project/pipe/pcaps/in{a}.pcap -c /home/ak/projects/major_project/pipe/logs/out{a}.csv")
    ids()

def ids():
    model = tf.keras.models.load_model('/home/ak/projects/major_project/mpui/console/MyModel5')
    csv_files = []
    for dirname, _, filenames in os.walk('/home/ak/projects/major_project/pipe/logs/'):
        for filename in filenames:
            csv_file = os.path.join(dirname, filename)
            print(os.path.join(dirname, filename))
            csv_files.append(csv_file)
    csv_files.sort()
    csv_files1 = csv_files[:-1]
    
    df = pd.concat([pd.read_csv(file) for file in csv_files1], ignore_index=True)
    df.columns = df.columns.str.strip()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.iloc[:,[3,6,11,12,13,14,15,16,17,18,19,20,21,22,7,8,32,35,33,34,36,39,40,37,38,41,44,45,42,43,46,47,48,49,28,29,9,10,24,23,25,26,27,50,51,52,53,54,55,77,56,57,58,75,76,28,69,70,73,71,72,74,78,80,79,81,59,60,
    31,30,63,64,61,62,67,68,65,66]]
    df = df.astype("float32")
    for file in csv_files1:
        os.system(f"mv {file} /home/ak/projects/major_project/pipe/logdone")

    #preparing the live data for the model

    dict = {0:'BENIGN', 1: 'Bot', 2: 'DDoS', 3: 'DoS', 4: 'PortScan'}
    scaler = MinMaxScaler()
    x = scaler.fit_transform(df)
    x.shape
    x2 = x.reshape(x.shape[0],1,x.shape[1])
    x2.shape
    dataset = tf.data.Dataset.from_tensor_slices(x2).batch(1)
    lii = []
    li = []
    i = 0

    #running prediction on the live dataset

    for data in dataset:
        pred = model.predict(data)
        if np.argmax(pred)>0 :
            lii.append(i)
            li.append(np.argmax(pred))
        i+=1
    new = []
    for i in li:
        new.append(dict[i])
    #appending to the threat.csv
    fin = df.iloc[lii].copy()
    fin['Label'] = new
    n = len(fin['Label'])
    if n > 0:
        notification.notify(
            title = "Threat Alert",
            message = f"{n} Threats have been detected, Please Download Report",
            timeout = 5
        )
        yam = AudioSegment.from_file('/home/ak/projects/major_project/mpui/yam.wav')
        play(yam)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    fin['Date'] = current_time
    fin.to_csv('/home/ak/projects/major_project/pipe/threats/threat.csv', mode='a', index=False, header=False)



def main(i):
    #generating the tcpdump
    command = f"sudo timeout 30 tcpdump -i any -w /home/ak/projects/major_project/pipe/pcaps/in{i+1}.pcap"
    os.system(command)
    cic(i+1)

def main2():
    #this is for the uploaded pcap process, the folders are in a different place to avoid a mess
    os.system(f"cicflowmeter -f /home/ak/projects/major_project/pipe/uppcaps/curr -c /home/ak/projects/major_project/pipe/logs2/out.csv")
    model = tf.keras.models.load_model('/home/ak/projects/major_project/mpui/console/MyModel5')
    csv_files = []
    for dirname, _, filenames in os.walk('/home/ak/projects/major_project/pipe/logs2/'):
        for filename in filenames:
            csv_file = os.path.join(dirname, filename)
            print(os.path.join(dirname, filename))
            csv_files.append(csv_file)
    csv_files.sort()
    csv_files1 = csv_files
    
    df = pd.concat([pd.read_csv(file) for file in csv_files1], ignore_index=True)
    df.columns = df.columns.str.strip()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.iloc[:,[3,6,11,12,13,14,15,16,17,18,19,20,21,22,7,8,32,35,33,34,36,39,40,37,38,41,44,45,42,43,46,47,48,49,28,29,9,10,24,23,25,26,27,50,51,52,53,54,55,77,56,57,58,75,76,28,69,70,73,71,72,74,78,80,79,81,59,60,
    31,30,63,64,61,62,67,68,65,66]]
    df = df.astype("float32")
    # for file in csv_files1:
    #     os.system(f"mv {file} /home/ak/projects/major_project/pipe/logdone")

    #preparing the live data for the model

    dict = {0:'BENIGN', 1: 'Bot', 2: 'DDoS', 3: 'DoS', 4: 'PortScan'}
    scaler = MinMaxScaler()
    x = scaler.fit_transform(df)
    x.shape
    x2 = x.reshape(x.shape[0],1,x.shape[1])
    x2.shape
    dataset = tf.data.Dataset.from_tensor_slices(x2).batch(1)
    lii = []
    li = []
    i = 0

    #running prediction on the live dataset

    for data in dataset:
        pred = model.predict(data)
        if np.argmax(pred)>0 :
            lii.append(i)
            li.append(np.argmax(pred))
        i+=1
    new = []
    for i in li:
        new.append(dict[i])
    #appending to the threat.csv, the other uploaded pcap threats2 csv
    fin = df.iloc[lii].copy()
    fin['Label'] = new
    n = len(fin['Label'])
    notification.notify(
        title = "Threat Alert",
        message = f"{n} Threats have been detected",
        timeout = 3
    )
    fin.to_csv('/home/ak/projects/major_project/pipe/threats2/threat.csv', mode='a', index=False, header=False)



    

    

