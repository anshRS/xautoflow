part of 'chat_bloc.dart';

class ChatState {
  final List<MessageEntity> messages;
  final bool isTyping;

  const ChatState({required this.messages, this.isTyping = false});

  ChatState copyWith({List<MessageEntity>? messages, bool? isTyping}) {
    return ChatState(
      messages: messages ?? this.messages,
      isTyping: isTyping ?? this.isTyping,
    );
  }
}
