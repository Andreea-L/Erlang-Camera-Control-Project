import numpy as np

f = open("roundtrip_timing.time")
f_agg = open("aggregator_timing.time")
lines = f.readlines()
agg_lines = f_agg.readlines()

lines = [line for line in lines if line!=""]

val = [ x.split(":") for x in lines	]
val_agg = [ x.split(":") for x in agg_lines ]

sends = [ x for x in val if x[0]=="s" ]
recs = [ x for x in val if x[0]=="r" ]
aggs = [ x for x in val_agg if x[0]=="a" ]
print sends
print aggs
time_to_rec = [ int(x[2])-int(y[2]) for x,y in zip(recs,sends) if x[1]==y[1]]
time_to_agg = [ int(x[2])-int(y[2]) for x,y in zip(aggs,sends) if x[1]==y[1]]

print "Avg. aggregation time: ",sum(time_to_agg)/len(time_to_agg)


det_f = open("detection_timing.time")
pub_f = open("publishing_timing.time")
det_times = [ int(line) for line in det_f.readlines() ]
pub_times = [ int(line) for line in pub_f.readlines() ]
print "Avg. detection time: ",sum(det_times)/len(det_times)
print "Avg. publishing time: ",sum(pub_times)/len(pub_times)