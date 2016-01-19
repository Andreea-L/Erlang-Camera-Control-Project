-module(face_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-import(lists, [append/2]).
-export([start_link/1]).
-export([init/1]).

-define(SERVER, ?MODULE).
-define(CHILD(I, Name, Type), {Name, {I, start_link, [Name]}, permanent, 5000, Type, [I]}).


% Supervisor for face detection processes


start_link(Args) ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, Args),
	Ref.

% Recursively starts "Times" x face detection processes
init(Args) -> 
	Times = lists:nth(1, Args),
	init(Times, []).

init(0, Acc) -> 
	{ok, {{one_for_one, 1, 1}, Acc}};
init(Times, Acc) ->
	ChildSpec = ?CHILD(face_server, Times, worker),
	% ChildSpec = {Times, {face_server, start_link, [Times]},
	%			 permanent, 2000, worker, [face_server]},
	init(Times-1, append(Acc, [ChildSpec])).