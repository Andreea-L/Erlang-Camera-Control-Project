
% This module runs the aggregator processes for the Erlang facetracking system.
% It is implemented as a generic server that receives faces, aggregates them and sends the face
% to a Python camera control module.
% 
% Author: Andreea Lutac

-module(aggregator_server).
-author('andreea.lutac').
-import(lists, [nth/2, sum/1]).
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

% Initialize the server with a new Python interpreter instance and a new Queue
init([]) -> 
  Faces_Q=queue:new(),
  {ok, PyInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject/Supervised"}]),
  {ok, [Faces_Q,PyInstance]}.

stop() ->
	gen_server:cast(self(), stop).
	
% Interface function for receving a face
aggregate({face, Face}) ->
  gen_server:cast(self(), {face, Face}).

% Update and trim queue to a specific length (i.e. 3), if necessary
update_queue(Faces_Q, Face) ->
  case queue:len(Faces_Q)==3 of
        true ->
          F1 = queue:drop(Faces_Q),
          F2 = queue:in(Face, F1),
          F2;
        false ->
          F2 = queue:in(Face, Faces_Q),
          F2
  end.

% Asynchronous handler for incoming faces; faces are pattern matched to ensure correctness
% and then aggregated into one mean rectangle circumscribing the "best" faces
handle_cast({face, FID, WorkerPID, Face}, State) ->
  Q = update_queue(nth(1,State), Face),
  Faces_L = queue:to_list(Q),
  BestX = [ nth(1,L) ||  L <- Faces_L, length(L)>0 ],
  BestY = [ nth(2,L) ||  L <- Faces_L, length(L)>0 ],
  BestHW = [ nth(3,L) ||  L <- Faces_L, length(L)>0 ],

  if 
    length(BestX)>0 ->
      BestFace = {round(sum(BestX)/length(BestX)), 
                  round(sum(BestY)/length(BestY)), 
                  round(sum(BestHW)/length(BestHW)), 
                  round(sum(BestHW)/length(BestHW))},

      % Send the best face to the Python tracking function
      python:call(nth(2,State), facetracking, track_face, [BestFace]);
    true ->
      io:format("No faces.~n", []),
      ok
  end,
  {noreply, [Q,nth(2, State)]};
	
% Synchronous message handler
handle_call(get_face, _From, State) -> 
  {noreply, State}.

% "!" message handler
handle_info(_Message, State) ->
  {noreply, State}.

terminate(_Reason, _Faces_Q) -> ok.
code_change(_OldVersion, State, _Extra) -> {ok, State}.