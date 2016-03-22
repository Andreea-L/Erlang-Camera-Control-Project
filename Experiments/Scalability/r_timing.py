import numpy as np

f = open("roundtrip_timing.time")
f_agg = open("aggregator_timing.time")
f_send = open("send_timing.time")
lines = f.readlines()
agg_lines = f_agg.readlines()
send_lines = f_send.readlines()

lines = [line for line in lines if line!=""]

val = [ x.split(":") for x in lines	]
val_agg = [ x.split(":") for x in agg_lines ]
val_send = [ x.split(":") for x in send_lines ]

sends = [ x for x in val_send if x[0]=="s" ]
recs = [ x for x in val if x[0]=="r" ]
sends_f = [ x for x in val if x[0]=="d" ]
aggs = [ x for x in val_agg if x[0]=="a" ]
#print recs
print zip(aggs,sends)
time_to_rec = [ int(x[2])-int(y[2]) for x,y in zip(recs,sends) if x[1]==y[1]]
time_to_agg = [ int(x[3])-int(y[2]) for x in aggs for y in sends_f if int(x[2])==int(y[1]) ]
time_to_detect = [ int(x[2])-int(y[2]) for x,y in zip(sends_f,recs) if int(x[1])==int(y[1]) ]
total_time = [ int(x[3])-int(y[2]) for x in aggs for y in sends if int(x[2])==int(y[1]) ]

print len(sends), len(aggs)
print "Avg. total time: ",sum(total_time)/(len(total_time)*1000.0)
print "Avg. receipt time: ",sum(time_to_rec)/(len(time_to_rec)*1000.0)
print "Avg. aggregation time: ",sum(time_to_agg)/(len(time_to_agg)*1000.0)
print "Avg. time to detect: ",sum(time_to_detect)/(len(time_to_detect)*1000.0)

# det_f = open("detection_timing.time")
# pub_f = open("publishing_timing.time")
# det_times = [ int(line) for line in det_f.readlines() ]
# pub_times = [ int(line) for line in pub_f.readlines() ]
# print "Avg. detection time: ",sum(det_times)/len(det_times)
# print "Avg. publishing time: ",sum(pub_times)/len(pub_times)