-module(chaos_monkey).
-author('andreea.lutac').
-import(lists, [nth/2, seq/2]).
-export([start/1, kill_sup/1]).

% Interface to start the entire face tracking program.
% Starts the topmost supervisor and makes initial calls to the Python interpreter responsible for supplying the image feed.
start(Args) ->
	KillN = nth(1, Args),
	WorkerN = nth(2, Args),
	io:format("Starting to kill random processes....~n",[]),
	kill(KillN, WorkerN).


kill(0, WorkerN) ->
	io:format("Finished killing processes.~n",[]);
	
kill(N, WorkerN) ->
	Proc = [ global:whereis_name(I) || I <- seq(1, WorkerN)],
	FilterProc = [ P || P <- Proc, P/=undefined ],
	io:format("Current processes: ~p~n", [FilterProc]),

	Rand = trunc(rand:uniform()*length(FilterProc)+1),
	io:format("Should kill: ~p, rand: ~p ~n", [nth(1,FilterProc), Rand]),

	%exit(nth(Rand,FilterProc), normal),
	[ gen_server:cast(P, stop) || P <- FilterProc ],

	T = os:system_time(),
	io:format("Killed: ~p at time ~p ~n", [nth(Rand,FilterProc),T]),
	{Result, Device} = file:open("/home/andreea/Documents/ErlangProject/Supervised/face_timing.time", [append]),
	io:format(Device, "~p~n", [T]),
	file:close(Device),

	timer:sleep(500),
	kill(N-1, WorkerN).

kill_sup(Type) ->
	if
		Type==top ->
			exit(whereis(top_supervisor), kill);
		Type==face ->
			exit(whereis(face_supervisor), kill);
		Type==agg ->
			exit(whereis(aggregator_supervisor), kill);
		true ->
			io:format("Unkown type. ~n",[])
	end,
	
	timer:sleep(5),
	io:format("Killed top supervisor. ~n", []).	

