part of 'chat_bloc.dart';

sealed class ChatEvent {}

// On Send Message Event
final class SendMessageEvent extends ChatEvent {
  final String text;

  SendMessageEvent(this.text);
}

// On Receive Message Event
final class MessageReceivedEvent extends ChatEvent {
  final MessageEntity message;

  MessageReceivedEvent(this.message);
}

// On Connect Chat Event
class ConnectChatEvent extends ChatEvent {
  final String userId;
  ConnectChatEvent(this.userId);
}

// On Disconnect Chat Event
class DisconnectChatEvent extends ChatEvent {}