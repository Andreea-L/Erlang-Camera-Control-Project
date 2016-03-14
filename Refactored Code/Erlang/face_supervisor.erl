
% This module encompasses the supervisor for the face detection processes
% 
% Author: Andreea Lutac

-module(face_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-import(lists, [append/2]).
-export([start_link/1]).
-export([init/1]).

% Macros to simplify child specification
-define(SERVER, ?MODULE).
-define(CHILD(I, Name, Type), {Name, {I, start_link, [Name]}, permanent, 5000, Type, [I]}).


start_link(Args) ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, Args),
	Ref.

% Recursively starts "Times" x face detection processes
init(Args) -> 
	Times = lists:nth(1, Args),
	init(Times, []).

init(0, Acc) -> 
	{ok, {{one_for_one, 1000, 1}, Acc}};
init(Times, Acc) ->
	ChildSpec = ?CHILD(face_server, Times, worker),
	init(Times-1, append(Acc, [ChildSpec])).