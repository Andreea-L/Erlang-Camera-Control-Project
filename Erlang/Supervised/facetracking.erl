-module(facetracking).
-author('andreea.lutac').
-import(lists, [nth/2, append/2]).
-import(random, [uniform/1]).
-export([aggregate_faces/1, detect_face/1, image_feed/1]).

% Code for the image feed, face detection and aggregation processes
% All three functions communicate both internally and to Python through message passing.

% Aggregation of detected faces
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

% Supplies frames to Python and receives Face tuples
detect_face(Aggregator) ->
	{ok, FaceInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	receive
		{frame, Frame} ->
			%io:format("ERL-DETECT-~p: Sending off. ~n",[self()]),
			python:call(FaceInstance, test, detect_face, [self(), Frame]),
			detect_face(Aggregator);
		{face, Face} when is_tuple(Face) ->
			%io:format("ERL-DETECT-~p: Face ~p received. ~n",[self(), FaceCounter]),
			Aggregator ! Face,
			detect_face(Aggregator);
		_Other ->
			io:format("ERL-DETECT~p: Unknown message: ~p~n",[self(),_Other]),
			detect_face(Aggregator)

	end.

% Receives frames from image feed
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


% start(Args) ->
% 	DeviceID = nth(1, Args),
% 	MainN = nth(2, Args),
% 	DetectorsN = nth(3, Args),
% 	{ok, FeedInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
% 	io:format("Arguments: ~p~n", [Args]),

% 	Aggregator = spawn_listeners(1, aggregate_faces, [queue:new()]),
% 	io:format("Aggregator: ~p~n", [Aggregator]),
% 	FaceFeeds = spawn_listeners(DetectorsN, detect_face, [0,0, Aggregator]),
% 	io:format("Face feeds: ~p~n", [FaceFeeds]),
% 	ImageFeeds = spawn_listeners(MainN, image_feed, [FaceFeeds]),
% 	io:format("Image feeds: ~p~n", [ImageFeeds]),
	
% 	% Feed = python:call(PythonInstance, test, open_webcam_feed, [DeviceID]),
% 	% io:format(Feed)
% 	python:call(FeedInstance, test, read_webcam_feed, [ImageFeeds, DeviceID]).
% 	