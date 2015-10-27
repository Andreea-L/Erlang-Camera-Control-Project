-module(facetracking).
-author('andreea.lutac').
-export ([set_up_feed/0]).



set_up_feed() ->
	DeviceID = 0,
	{ok, PythonInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	% Feed = python:call(PythonInstance, test, open_webcam_feed, [DeviceID]),
	% io:format(Feed),
	Frame = python:call(PythonInstance, test, read_webcam_feed, [DeviceID]),
	io:format(is_list(Frame)),
	Face = python:call(PythonInstance, test, detect_face, [Frame]),
	io:format(is_tuple(Face)).
	%python:stop(PythonInstance).
