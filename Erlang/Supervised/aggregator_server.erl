-module(aggregator_server).
-author('andreea.lutac').
%-define(SERVER, ?MODULE).
-export([                      
  start_link/0, 
  stop/0,
  aggregate/1,
  get_face/0]).
-export([ 
  init/1, 
  handle_call/3, 
  handle_cast/2,   
  handle_info/2,              
  terminate/2,                 
  code_change/3]).


start_link() ->
    gen_server:start_link({global, ?MODULE}, ?MODULE, [], []).

stop() ->
	gen_server:cast(self(), stop).
	
aggregate({face, Face}) ->
  gen_server:cast(self(), {face, Face}).

get_face() ->
  gen_server:call(self(), get_face).

init([]) ->
	Faces_Q=queue:new(),
  {ok, Faces_Q}.

handle_cast({face, Face}, Faces_Q) ->
	case queue:len(Faces_Q)==10 of
        true ->
          F1 = queue:drop(Faces_Q),
          F2 = queue:in(Face, F1),
          {noreply, F2};
        false ->
          F2 = queue:in(Face, Faces_Q),
          {noreply, F2}
  end;

handle_cast(stop, Faces_Q) ->
	{stop, normal, Faces_Q}.

handle_call(get_face, _From, Faces_Q) -> 
  {noreply, Faces_Q}.

handle_info(_Message, Faces_Q) -> {noreply, Faces_Q}.
terminate(_Reason, _Faces_Q) -> ok.
code_change(_OldVersion, Faces_Q, _Extra) -> {ok, Faces_Q}.