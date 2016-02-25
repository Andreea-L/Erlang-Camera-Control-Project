-module(top_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-export([start_link/1]).
-import(lists, [nth/2]).
-export([init/1]).

-define(SERVER, ?MODULE).
-define(CHILD(I, Name, Type, Args), {Name, {supervisor, start_link, [{local, Name}, Name, Args]}, permanent, 5000, Type, [I]}).

% Topmost supervisor.
% Supervises: the image feed supervisor, the face detection supervisor and the aggregator supervisor

start_link(Args) ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, Args),
	Ref.

% Start children with specific arguments
init(Args) ->
	T = os:system_time(),
	io:format("Start time of top_supervisor: ~p ~n",[T]),
	%erlang:write_file(top_sup_timing, T, [append]),
	FacesN = nth(1, Args),
	Aggregator = ?CHILD(aggregator_supervisor, aggregator_supervisor, supervisor, []),
	Faces = ?CHILD(face_supervisor, face_supervisor, supervisor, [FacesN]),

	{ok, {{one_for_one, 1000, 1}, [Faces, Aggregator]}}.