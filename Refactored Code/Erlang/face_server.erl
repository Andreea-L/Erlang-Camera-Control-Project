
% This module runs the main face detection processes for the Erlang facetracking system.
% It is implemented as a generic server that receives frames and passes them on
% to a Python face detection module.
% 
% Author: Andreea Lutac

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

% Initialize the server with a new Python interpreter instance
init([]) ->
  {ok, PyInstance} = python:start([{python_path, "/home/andreea/Documents/ErlangProject/Supervised"}]),
  {ok, PyInstance}.

stop() ->
	gen_server:cast(self(), stop).

% Interface function for receving a frame
image_feed({frame, Frame}) ->
	gen_server:cast(self(), {frame, Frame}).

% Asynchronous handler for incoming frames; frames are pattern matched to ensure correctness
handle_cast({frame,FID, Frame}, PyInstance) ->
	python:call(PyInstance, facetracking, detect_face, [Frame, FID,self()]),
  {noreply, PyInstance};

% Synchronous message handler
handle_call(_Message, _From, PyInstance) -> {noreply, PyInstance}.

% "!" message handler
handle_info(_Message, PyInstance) ->
  {noreply, PyInstance}.

terminate(_Reason, _PyInstance) -> 
  python:stop(_PyInstance),
  ok.
code_change(_OldVersion, PyInstance, _Extra) -> {ok, PyInstance}.