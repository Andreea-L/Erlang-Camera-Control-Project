-module(interface).
-author('andreea.lutac').
-import(lists, [nth/2]).
-export([start/1]).

% Interface to start the entire face tracking program.
% Starts the topmost supervisor and makes initial calls to the Python interpreter responsible for supplying the image feed.
start(Args) ->
	{DeviceID, _} = string:to_integer(nth(1, Args)),
	{FacesN, _} = string:to_integer(nth(2, Args)),
	{ok, FeedInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject/Supervised"}]),
	io:format("Arguments: ~p~n", [Args]),

	{ok, TopSuper} = top_supervisor:start_link([FacesN]),
	io:format("Supervision tree started. ~n", []),
	python:call(FeedInstance, facetracking_no_rt, read_webcam_feed, [FacesN, DeviceID]).	

