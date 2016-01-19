-module(aggregator_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-export([start_link/0]).
-export([init/1]).
-define(SERVER, ?MODULE).

% Supervisor for the face aggregation step

start_link() ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, []),
	Ref.

init(Args) ->
	ChildSpec = {aggregator_server, {aggregator_server, start_link, []},
				 permanent, 2000, worker, [aggregator_server]},
	{ok, {{one_for_one, 1, 1}, [ChildSpec]}}.