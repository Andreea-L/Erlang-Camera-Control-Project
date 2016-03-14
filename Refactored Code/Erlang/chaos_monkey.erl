
% This module encompasses the "chaos monkey" program used to randomly terminate/kill processes
% 
% Author: Andreea Lutac

-module(chaos_monkey).
-author('andreea.lutac').
-import(lists, [nth/2, seq/2]).
-export([start/1, kill_sup/1]).


start(Args) ->
	KillN = nth(1, Args),
	WorkerN = nth(2, Args),
	KillType = nth(3, Args),
	io:format("Starting to kill random processes....~n",[]),
	kill(KillN, WorkerN, KillType).


kill(0, WorkerN, KillType) ->
	io:format("Finished killing processes.~n",[]);
	
kill(N, WorkerN, KillType) ->
	Proc = [ global:whereis_name(I) || I <- seq(1, WorkerN)],
	FilterProc = [ P || P <- Proc, P/=undefined ],
	Rand = trunc(rand:uniform()*length(FilterProc)+1),

	case KillType of
		stop ->
			nth(Rand,FilterProc) ! KillType;
		kill ->
			exit(nth(Rand,FilterProc),kill)
	end,

	kill(N-1, WorkerN, KillType).

kill_sup(Type) ->
	if
		Type==top ->
			gen_server:cast(whereis(top_supervisor), stop);
		Type==face ->
			gen_server:cast(whereis(face_supervisor), stop);
		Type==agg ->
			gen_server:cast(whereis(aggregator_supervisor), stop);
		true ->
			io:format("Unkown type. ~n",[])
	end,
	
	timer:sleep(5),
	io:format("Killed supervisor. ~n", []).	

