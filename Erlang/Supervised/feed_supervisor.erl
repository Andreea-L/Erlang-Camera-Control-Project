-module(feed_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-import(lists, [append/2]).
-export([start_link/1]).
-export([init/1]).
-define(SERVER, ?MODULE).

% Supervisor for image feed processes

start_link(Args) ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, [Args]),
	Ref.


% Recursively starts "Times" x image feed processes
init(Args) -> 
	Times = lists:nth(1, Args),
	FuncArgs = lists:delete(Times, Args),
	init(Times, FuncArgs, []).

init(0, FuncArgs, Acc) -> 
	{ok, {{one_for_one, 1, 1}, Acc}};
init(Times, FuncArgs, Acc) ->
	ChildSpec = {Times, {facetracking, image_feed, [FuncArgs]},
				 permanent, 2000, worker, [facetracking]},
	init(Times-1, FuncArgs, append(Acc, [ChildSpec])).