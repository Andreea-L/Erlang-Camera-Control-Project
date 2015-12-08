-module(top_supervisor).
-author('andreea.lutac').
-behaviour(supervisor).
-export([start_link/2]).
-import(lists, [nth/2]).
-export([init/1]).
-define(SERVER, ?MODULE).

% Topmost supervisor.
% Supervises: the image feed supervisor, the face detection supervisor and the aggregator supervisor

start_link(FeedN, FacesN) ->
	Ref = supervisor:start_link({local, ?SERVER}, ?MODULE, [FeedN, FacesN]),
	Ref.

% Start children with specific arguments
init(Args) ->
	FeedN = nth(1, Args),
	FacesN = nth(1, Args),
	Aggregator = {agg_super, {aggregator_supervisor, start_link, []},
				 permanent, 2000, worker, [aggregator_supervisor]},
	Faces = {face_super, {face_supervisor, start_link, [FacesN,Aggregator]},
				 permanent, 2000, worker, [face_supervisor]},

	FacesProc = supervisor:which_children(Faces),
	FacesPIDs = lists:map(fun({_, PID, _, _}) -> PID end, FacesProc),
	Feed = {feed_super, {feed_supervisor, start_link, [FeedN,FacesPIDs]},
			permanent, 2000, worker, [feed_supervisor]},
	
	
	{ok, {{one_for_one, 1, 1}, [Feed, Faces, Aggregator]}}.