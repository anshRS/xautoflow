import 'dart:async';

import 'package:client/common/entities/message.dart';
import 'package:client/features/chat/domain/usecases/connect_chat_usecase.dart';
import 'package:client/features/chat/domain/usecases/disconnect_chat_usecase.dart';
import 'package:client/features/chat/domain/usecases/send_message_usecase.dart';
import 'package:client/features/chat/domain/usecases/stream_message_usecase.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'chat_state.dart';
part 'chat_event.dart';

class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final SendMessageUsecase _sendMessageUsecase;
  final StreamMessageUsecase _streamMessageUsecase;
  StreamSubscription? _subscription;
  final ConnectChatUsecase _connectChatUsecase;
  final DisconnectChatUsecase _disconnectChatUsecase;

  ChatBloc({
    required SendMessageUsecase sendMessageUsecase,
    required StreamMessageUsecase streamMessageUsecase,
    required ConnectChatUsecase connectChatUsecase,
    required DisconnectChatUsecase disconnectChatUsecase,
  }) : _sendMessageUsecase = sendMessageUsecase,
       _streamMessageUsecase = streamMessageUsecase,
       _connectChatUsecase = connectChatUsecase,
       _disconnectChatUsecase = disconnectChatUsecase,
       super(ChatState(messages: [])) {
    on<SendMessageEvent>(_onSendMessage);
    on<MessageReceivedEvent>(_onMessageReceived);
    on<ConnectChatEvent>(_onConnectChat);
    on<DisconnectChatEvent>(_onDisconnectChat);
  }

  void _onSendMessage(SendMessageEvent event, Emitter<ChatState> emit) {
    final msg = MessageEntity(data: event.text, isBot: false);
    _sendMessageUsecase(SendMessageParams(message: event.text));
    emit(state.copyWith(messages: [msg, ...state.messages], isTyping: true));
  }

  void _onMessageReceived(MessageReceivedEvent event, Emitter<ChatState> emit) {
    emit(
      state.copyWith(
        messages: [event.message, ...state.messages],
        isTyping: false,
      ),
    );
  }

  void _onConnectChat(ConnectChatEvent event, Emitter<ChatState> emit) async {
    await _connectChatUsecase(ConnectParams(userId: event.userId));
    _subscription = _streamMessageUsecase(NoParams()).listen((message) {
      add(MessageReceivedEvent(message));
    });
  }

  void _onDisconnectChat(DisconnectChatEvent event, Emitter<ChatState> emit) {
    _subscription?.cancel();
    _subscription = null;
    _disconnectChatUsecase();
  }
}
