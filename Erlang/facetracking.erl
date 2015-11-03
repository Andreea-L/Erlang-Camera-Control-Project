-module(facetracking).
-author('andreea.lutac').
-export([start/0, detect_face/1, listen_for_images/1]).


detect_face(PythonInstance) ->
	receive
		Frame when is_list(Frame) ->
			io:format("ERL: Received frame ~n",[]),
			Face = python:call(PythonInstance, test, detect_face, [Frame]),
			io:format("ERL: Face received.~n",[])

	end.

listen_for_images(Detector_PID) ->
	receive
		error ->
			io:format("ERL: Error receiving frame.~n",[]);
		Frame when is_list(Frame) ->
			io:format("ERL: Received frame ~n",[]),
			Detector_PID ! Frame,
			listen_for_images(Detector_PID);
		_Other ->
			io:format("ERL: Unknown message: ~p, ~p~n",[_Other, is_atom(_Other)])
	end.

start() ->
	DeviceID = 1,
	{ok, PythonInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),

	Detector_PID = spawn(facetracking, detect_face, [PythonInstance]),
	Listener_PID = spawn(facetracking, listen_for_images, [Detector_PID]),
	
	% Feed = python:call(PythonInstance, test, open_webcam_feed, [DeviceID]),
	% io:format(Feed)

	python:call(PythonInstance, test, read_webcam_feed, [Listener_PID, DeviceID]).
