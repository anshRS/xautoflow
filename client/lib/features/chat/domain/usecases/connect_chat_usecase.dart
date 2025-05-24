import 'package:client/features/chat/domain/repositories/chat_repository.dart';

class ConnectChatUsecase {
  final ChatRepository chatrepository;

  ConnectChatUsecase(this.chatrepository);

  Future<void> call(ConnectParams params) {
    return chatrepository.connect(params.userId);
  }
}

class ConnectParams {
  final String userId;

  ConnectParams({required this.userId});
}