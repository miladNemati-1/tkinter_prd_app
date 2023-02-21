import pandas as pd
from syringepump import SyringePump as Pump
import time
duration = []
fr = []
times = []
df = pd.read_csv('code_Parameters.csv')

def calc_time():
    # time=[]
    for index, row in df.iterrows():
        start_min = row['Start_min']
        stop_min = row['Stop_min']
        dead_volume1 = row['DeadVolume1(min)']
        dead_volume2 = row['DeadVolume1(min)']
        dead_volume3 = row['DeadVolume1(min)']
        sta_time = row['StabilisationTime']
        res = stop_min-start_min+dead_volume1+dead_volume2+dead_volume3+sta_time
        duration.append(res)
        times.append([start_min, stop_min, dead_volume1,
                     dead_volume2, dead_volume3, sta_time])


def calc_fr():
    # fr=[]
    for index, row in df.iterrows():
        start_fr = row['StartFR']
        stop_fr = row['StopFR']
        fr.append([start_fr, stop_fr])

def run():
    pump = Pump('COM1', name='my_pump')


    calc_time()
    calc_fr()
    # print('time', times)
    # print('fr changes', fr)
    # print('duration', duration)

    start_time = times[0][0]
    print('start_time', start_time)

    start_time = time.time()

    started = False
    changed_end_flow_rate = False

    i = 0
    pump.changeFlowrate(fr[i][0])
    pump.start()
    changed_fr = False
    spent_time = 0
    print(len(times))
    while i < len(times):
        current_time = time.time()

        if (time.time()-start_time)/60 >= 1.3 and i == 0 and not changed_fr:
            pump.changeFlowrate(fr[i][1])
            changed_fr = True
            spent_time += 1.3
            start_time = time.time()
            print("first if loop")
        # print("i:", i)
        # print("duration till now: ", (time.time()-start_time)/60)

        if (time.time()-start_time)/60 >= times[i][2]+times[i][1] and changed_fr:
            i += 1
            if i != len(times):
                pump.changeFlowrate(fr[i][1])
                print(fr[i][1])
            start_time = time.time()
            print("herer")
            print("i: ", i)

    pump.stop()
