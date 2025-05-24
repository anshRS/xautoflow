import 'package:client/features/chat/data/datasources/chat_remote_datasource.dart';
import 'package:client/common/entities/message.dart';
import 'package:client/features/chat/domain/repositories/chat_repository.dart';

class ChatRepositoryImpl implements ChatRepository {
  final ChatRemoteDatasource remoteDatasource;

  ChatRepositoryImpl(this.remoteDatasource);

  @override
  void sendMessage(String message) {
    return remoteDatasource.sendMessage(message);
  }

  @override
  Stream<MessageEntity> getMessage() {
    return remoteDatasource.messageStream;
  }

  @override
  Future<void> connect(String userId) {
    return remoteDatasource.connect(userId);
  }

  @override
  void disconnect() {
    remoteDatasource.dispose();
  }
}
