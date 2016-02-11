import numpy as np

f = open("roundtrip_timing_py.time")
f_erl = open("roundtrip_timing_erl.time")
#f_agg = open("aggregator_timing.time")
lines = f.readlines()+f_erl.readlines()
#gg_lines = f_agg.readlines()

lines = [line for line in lines if line!=""]

val = [ x.split(":") for x in lines	]
#val_agg = [ x.split(":") for x in agg_lines ]

frame_sends = [ x for x in val if x[0]=="PYs" ]
frame_recs = [ x for x in val if x[0]=="ERLr" ]
det_recs = [ x for x in val if x[0]=="PYg" ]
det_sends = [ x for x in val if x[0]=="PYf" ]
face_recs = [ x for x in val if x[0]=="ERLa" ]
#aggs = [ x for x in val_agg if x[0]=="a" ]
print frame_sends
print frame_recs
print det_recs
print det_sends
print face_recs
time_to_rec = [ int(x[2])-int(y[2]) for x in frame_recs for y in frame_sends if x[1]==y[1]]
time_to_rec_at_detector = [ int(x[2])-int(y[2]) for x in frame_recs for y in det_recs if x[1]==y[1]]
time_to_rec_at_agg = [ int(x[2])-int(y[2]) for x in det_sends for y in face_recs if x[1]==y[1]]
#time_to_agg = [ int(x[2])-int(y[2]) for x,y in zip(aggs,sends) if x[1]==y[1]]
print time_to_rec
print "Avg. frame receive time at Erlang: ",sum(time_to_rec)/(len(time_to_rec)*1000000.0)
print "Avg. frame receive time at Python: ",sum(time_to_rec_at_detector)/(len(time_to_rec_at_detector)*1000000.0)
print "Avg. face receive time at aggregator: ",sum(time_to_rec_at_agg)/(len(time_to_rec_at_agg)*1000000.0)


# det_f = open("detection_timing.time")
# pub_f = open("publishing_timing.time")
# det_times = [ int(line) for line in det_f.readlines() ]
# pub_times = [ int(line) for line in pub_f.readlines() ]
# print "Avg. detection time: ",sum(det_times)/len(det_times)
# print "Avg. publishing time: ",sum(pub_times)/len(pub_times)