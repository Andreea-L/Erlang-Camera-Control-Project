-module(facetracking).
-author('andreea.lutac').
-import(lists, [nth/2, append/2]).
-import(random, [uniform/1]).
-export([start/1, detect_face/0, image_feed/2]).


detect_face() ->
	receive
		Face when is_tuple(Face) ->
			io:format("ERL-DETECT-~p: Face received. ~n",[self()]),
			detect_face();
		_Other ->
			io:format("ERL-DETECT~p: Unknown message: ~p~n",[self(),_Other]),
			detect_face()

	end.

image_feed(PythonInstance, Detector_Pids) ->
	receive
		error ->
			io:format("ERL-FEED-~p: Error receiving frame.~n",[self()]);
		Frame when is_list(Frame) ->
			io:format("ERL-FEED-~p: Received frame ~n",[self()]),
			%PythonInstance ! [Detector_Pids, Frame],
			python:call(PythonInstance, test, start_detection, [Detector_Pids, Frame]),
			image_feed(PythonInstance, Detector_Pids);
		_Other ->
			io:format("ERL-FEED-~p: Unknown message: ~p~n",[self(),_Other]),
			image_feed(PythonInstance, Detector_Pids)
	end.


spawn_listeners(Times, Func, FuncArgs) -> spawn_listeners(Times, Func, FuncArgs, []).

spawn_listeners(0, Func, FuncArgs, Acc) -> Acc;
spawn_listeners(Times, Func, FuncArgs, Acc) ->
	Pid = spawn(facetracking, Func, FuncArgs),
	spawn_listeners(Times-1, Func, FuncArgs, append(Acc, [Pid])).


start(Args) ->
	DeviceID = nth(1, Args),
	MainN = nth(2, Args),
	DetectorsN = nth(3, Args),
	{ok, PythonInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	io:format("Arguments: ~p~n", [Args]),
	FaceFeeds = spawn_listeners(DetectorsN, detect_face, []),
	io:format("Face feeds: ~p~n", [FaceFeeds]),
	ImageFeeds = spawn_listeners(MainN, image_feed, [PythonInstance, FaceFeeds]),
	io:format("Image feeds: ~p~n", [ImageFeeds]),
	
	% Feed = python:call(PythonInstance, test, open_webcam_feed, [DeviceID]),
	% io:format(Feed)
	python:call(PythonInstance, test, start_feed, [ImageFeeds, DeviceID]).
	