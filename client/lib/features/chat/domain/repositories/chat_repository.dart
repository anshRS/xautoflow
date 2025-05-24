import 'package:client/common/entities/message.dart';

abstract interface class ChatRepository {
  Future<void> connect(String userId);
  void sendMessage(String message);
  Stream<MessageEntity> getMessage();
  void disconnect();
}