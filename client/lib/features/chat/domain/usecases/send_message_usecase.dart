import 'package:client/features/chat/domain/repositories/chat_repository.dart';

class SendMessageUsecase {
  final ChatRepository chatRepository;

  const SendMessageUsecase(this.chatRepository);

  void call(SendMessageParams params) {
    return chatRepository.sendMessage(params.message);
  }
}

class SendMessageParams {
  final String message;

  SendMessageParams({
    required this.message
  });
}