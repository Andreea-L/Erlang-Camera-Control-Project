-module(facetracking).
-author('andreea.lutac').
-import(lists, [nth/2, append/2]).
-import(random, [uniform/1]).
-export([start/1, aggregate_faces/1, detect_face/3, image_feed/1]).


aggregate_faces(Faces_Q) ->
	receive
		Face when is_tuple(Face) ->
			case queue:len(Faces_Q)==10 of
				true ->
					F1 = queue:drop(Faces_Q),
					F2 = queue:in(Face, F1),
					aggregate_faces(F2);
				false ->
					F2 = queue:in(Face, Faces_Q),
					aggregate_faces(F2)
			end

	end.

detect_face(FrameCounter, FaceCounter, Aggregator) ->
	{ok, FaceInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	receive
		{frame, Frame} ->
			io:format("ERL-DETECT-~p: Sending off ~p. ~n",[self(), FrameCounter]),
			python:call(FaceInstance, test, detect_face, [self(), Frame]),
			detect_face(FrameCounter + 1, FaceCounter, Aggregator);
		{face, Face} when is_tuple(Face) ->
			io:format("ERL-DETECT-~p: Face ~p received. ~n",[self(), FaceCounter]),
			Aggregator ! Face,
			detect_face(FrameCounter, FaceCounter+1, Aggregator);
		_Other ->
			io:format("ERL-DETECT~p: Unknown message: ~p~n",[self(),_Other]),
			detect_face(FrameCounter, FaceCounter, Aggregator)

	end.

image_feed(Detector_Pids) ->
	receive
		error ->
			io:format("ERL-FEED-~p: Error receiving frame.~n",[self()]);
		{frame,Frame} ->
			%io:format("ERL-FEED-~p: Received frame ~n",[self()]),
			[Pid ! {frame, Frame} || Pid<-Detector_Pids],
			image_feed(Detector_Pids);
		_Other ->
			io:format("ERL-FEED-~p: Unknown message: ~p~n",[self(),_Other]),
			image_feed(Detector_Pids)
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
	{ok, FeedInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	io:format("Arguments: ~p~n", [Args]),

	Aggregator = spawn_listeners(1, aggregate_faces, [queue:new()]),
	io:format("Aggregator: ~p~n", [Aggregator]),
	FaceFeeds = spawn_listeners(DetectorsN, detect_face, [0,0, Aggregator]),
	io:format("Face feeds: ~p~n", [FaceFeeds]),
	ImageFeeds = spawn_listeners(MainN, image_feed, [FaceFeeds]),
	io:format("Image feeds: ~p~n", [ImageFeeds]),
	
	% Feed = python:call(PythonInstance, test, open_webcam_feed, [DeviceID]),
	% io:format(Feed)
	python:call(FeedInstance, test, read_webcam_feed, [ImageFeeds, DeviceID]).
	