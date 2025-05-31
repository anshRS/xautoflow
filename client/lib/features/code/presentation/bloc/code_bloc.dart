import 'dart:async';

import 'package:client/common/entities/message.dart';
import 'package:client/features/code/domain/usecases/connect_code_usecase.dart';
import 'package:client/features/code/domain/usecases/disconnect_code_usecase.dart';
import 'package:client/features/code/domain/usecases/send_message_usecase.dart';
import 'package:client/features/code/domain/usecases/stream_message_usecase.dart';
import 'package:flutter_bloc/flutter_bloc.dart';


part 'code_state.dart';
part 'code_event.dart';

class CodeBloc extends Bloc<CodeEvent, CodeState> {
  final SendMessageUsecase _sendMessageUsecase;
  final StreamMessageUsecase _streamMessageUsecase;
  StreamSubscription? _subscription;
  final ConnectCodeUsecase _connectCodeUsecase;
  final DisconnectCodeUsecase _disconnectCodeUsecase;

  CodeBloc({
    required SendMessageUsecase sendMessageUsecase,
    required StreamMessageUsecase streamMessageUsecase,
    required ConnectCodeUsecase connectCodeUsecase,
    required DisconnectCodeUsecase disconnectCodeUsecase,
  }) : _sendMessageUsecase = sendMessageUsecase,
       _streamMessageUsecase = streamMessageUsecase,
       _connectCodeUsecase = connectCodeUsecase,
       _disconnectCodeUsecase = disconnectCodeUsecase,
       super(CodeState(messages: [])) {
    on<SendMessageEvent>(_onSendMessage);
    on<MessageReceivedEvent>(_onMessageReceived);
    on<ConnectCodeEvent>(_onConnectCode);
    on<DisconnectCodeEvent>(_onDisconnectCode);
  }

  void _onSendMessage(SendMessageEvent event, Emitter<CodeState> emit) {
    final msg = MessageEntity(data: event.text, isBot: false);
    _sendMessageUsecase(SendMessageParams(message: event.text));
    emit(state.copyWith(messages: [msg, ...state.messages], isTyping: true));
  }

  void _onMessageReceived(MessageReceivedEvent event, Emitter<CodeState> emit) {
    emit(
      state.copyWith(
        messages: [event.message, ...state.messages],
        isTyping: false,
      ),
    );
  }

  void _onConnectCode(ConnectCodeEvent event, Emitter<CodeState> emit) async {
    await _connectCodeUsecase(ConnectParams(userId: event.userId));
    _subscription = _streamMessageUsecase(NoParams()).listen((message) {
      add(MessageReceivedEvent(message));
    });
  }

  void _onDisconnectCode(DisconnectCodeEvent event, Emitter<CodeState> emit) {
    _subscription?.cancel();
    _subscription = null;
    _disconnectCodeUsecase();
  }
}
