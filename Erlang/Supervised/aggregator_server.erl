-module(aggregator_server).
-author('andreea.lutac').
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
  T = os:system_time(),
  io:format("Start time of aggregator: ~p ~n",[T]),
  %erlang:write_file(agg_timing, T, [append]),
  Faces_Q=queue:new(),
  {ok, Faces_Q}.

handle_cast({face, FID, Face}, Faces_Q) ->
  %io:format("Got face. ~n", []),
  T = os:system_time(),
  {Result, Device} = file:open("/home/andreea/Documents/ErlangProject/Supervised/roundtrip_timing_erl.time", [append]),
  io:format(Device, "ERLa:~p:~p~n", [FID,T]),
  file:close(Device),
  Faces_L = queue:to_list(Faces_Q),

  BestX = [ lists:nth(1,L) ||  L <- Faces_L, length(L)>0 ],
  BestY = [ lists:nth(2,L) ||  L <- Faces_L, length(L)>0 ],
  BestHW = [ lists:nth(3,L) ||  L <- Faces_L, length(L)>0 ],

  if 
    length(BestX)>0 ->
      BestFace = {round(lists:sum(BestX)/length(BestX)), 
                  round(lists:sum(BestY)/length(BestY)), 
                  round(lists:sum(BestHW)/length(BestHW)), 
                  round(lists:sum(BestHW)/length(BestHW))},
      % {ok, PyInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject/Supervised"}]),
      % python:call(PyInstance, facetracking, display_face, [BestFace]);
      io:format("Best face: ~p~n", [BestFace]);
    true ->
      io:format("Best face: ~p~n", [[]])
      % ok
  end,

	case queue:len(Faces_Q)==100 of
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