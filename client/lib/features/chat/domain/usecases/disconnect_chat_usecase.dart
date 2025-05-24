import 'package:client/features/chat/domain/repositories/chat_repository.dart';

class DisconnectChatUsecase {
  final ChatRepository chatRepository;

  const DisconnectChatUsecase(this.chatRepository);

  void call() {
    chatRepository.disconnect();
  }

}