-module(interface).
-author('andreea.lutac').
-import(lists, [nth/2]).
-export([start/1]).

% Interface to start the entire face tracking program.
% Starts the topmost supervisor and makes initial calls to the Python interpreter responsible for supplying the image feed.
start(Args) ->
	DeviceID = nth(1, Args),
	MainN = nth(2, Args),
	DetectorsN = nth(3, Args),
	{ok, FeedInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
	io:format("Arguments: ~p~n", [Args]),

	{ok, TopSuper} = top_supervisor:start_link(MainN, DetectorsN),
	AllProc = supervisor:which_children(TopSuper),
	FeedPIDs = lists:map(fun({feed_super, PID, _, _}) -> PID end, AllProc),
	python:call(FeedInstance, test, read_webcam_feed, [FeedPIDs, DeviceID]).	

