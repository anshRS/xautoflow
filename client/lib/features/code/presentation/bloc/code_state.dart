part of 'code_bloc.dart';

class CodeState {
  final List<MessageEntity> messages;
  final bool isTyping;

  const CodeState({required this.messages, this.isTyping = false});

  CodeState copyWith({List<MessageEntity>? messages, bool? isTyping}) {
    return CodeState(
      messages: messages ?? this.messages,
      isTyping: isTyping ?? this.isTyping,
    );
  }
}
