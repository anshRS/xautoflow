import 'package:client/common/entities/message.dart';
import 'package:client/features/code/data/datasources/code_remote_datasource.dart';
import 'package:client/features/code/domain/repositories/code_repository.dart';

class CodeRepositoryImpl implements CodeRepository {
  final CodeRemoteDatasource remoteDatasource;

  CodeRepositoryImpl(this.remoteDatasource);

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
