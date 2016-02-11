-module(face_server).
-author('andreea.lutac').
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


init([]) ->
  T = os:system_time(),
  io:format("Start time of ~p : ~p ~n",[self(), T]),
  {Result, Device} = file:open("/home/andreea/Documents/ErlangProject/Supervised/face_timing.time", [append]),
  io:format(Device, "~p~n", [T]),
  io:format(Device, "~n", []),
	file:close(Device),

  {ok, PyInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject/Supervised"}]),
  {ok, PyInstance}.

handle_cast({frame,FID, Frame}, PyInstance) ->
  %io:format("Got frame at: ~p ~n", [self()]),
  T = os:system_time(),
  {Result, Device} = file:open("/home/andreea/Documents/ErlangProject/Supervised/roundtrip_timing_erl.time", [append]),
  io:format(Device, "ERLr:~p:~p~n", [FID,T]),
  file:close(Device),
	python:call(PyInstance, facetracking, detect_face, [Frame]),
  {noreply, PyInstance};

handle_cast(stop, PyInstance) ->
	{stop, normal, PyInstance}.

handle_call(_Message, _From, PyInstance) -> {noreply, PyInstance}.
handle_info(_Message, PyInstance) -> {noreply, PyInstance}.
terminate(_Reason, _PyInstance) -> ok.
code_change(_OldVersion, PyInstance, _Extra) -> {ok, PyInstance}.