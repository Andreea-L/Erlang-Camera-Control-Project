-module(feed_server).
-author('andreea.lutac').
%-define(SERVER, ?MODULE).
-export([                      
  start_link/1, 
  stop/0,        
  image_feed/1]).
-export([ 
  init/1, 
  handle_call/3, 
  handle_cast/2,   
  handle_info/2,              
  terminate/2,                 
  code_change/3]).


start_link(Name) ->
    gen_server:start_link({global, Name}, ?MODULE, [], []).

stop() ->
	gen_server:cast(self(), stop).

image_feed({frame, Frame}) ->
	gen_server:cast(self(), {frame, Frame}).
	
% aggregate({face, Face}) ->
%   gen_server:cast(self(), {face, Face})

init([]) ->
	{ok, PyInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject"}]),
  {ok, PyInstance}.

handle_cast({frame, Frame}, PyInstance) ->
	python:call(PyInstance, test, detect_face, [self(), Frame]);

% handle_cast({face, Face}, PyInstance) ->
% 	aggregator_server:aggregate(Face);

handle_cast(stop, PyInstance) ->
	{stop, normal, PyInstance}.

handle_call(_Message, _From, PyInstance) -> {noreply, PyInstance}.
handle_info(_Message, PyInstance) -> {noreply, PyInstance}.
terminate(_Reason, _PyInstance) -> ok.
code_change(_OldVersion, PyInstance, _Extra) -> {ok, PyInstance}.