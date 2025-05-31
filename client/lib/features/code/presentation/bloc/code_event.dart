part of 'code_bloc.dart';


sealed class CodeEvent {}

// On Send Message Event
final class SendMessageEvent extends CodeEvent {
  final String text;

  SendMessageEvent(this.text);
}

// On Receive Message Event
final class MessageReceivedEvent extends CodeEvent {
  final MessageEntity message;

  MessageReceivedEvent(this.message);
}

// On Connect Code Event
class ConnectCodeEvent extends CodeEvent {
  final String userId;
  ConnectCodeEvent(this.userId);
}

// On Disconnect Code Event
class DisconnectCodeEvent extends CodeEvent {}