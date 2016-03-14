
% This module encompasses the supervisor for the aggregator process
% 
% Author: Andreea Lutac

-module(aggregator_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-export([start_link/0]).
-export([init/1]).

-define(SERVER, ?MODULE).


start_link() ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, []),
	Ref.

init([]) ->
	ChildSpec = {aggregator_server, {aggregator_server, start_link, []},
				 permanent, 2000, worker, [aggregator_server]},
	{ok, {{one_for_one, 1000, 1}, [ChildSpec]}}.