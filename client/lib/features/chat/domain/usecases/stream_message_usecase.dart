import 'package:client/common/entities/message.dart';
import 'package:client/features/chat/domain/repositories/chat_repository.dart';

class StreamMessageUsecase {
  final ChatRepository chatRepository;

  const StreamMessageUsecase(this.chatRepository);

  Stream<MessageEntity> call(NoParams params) {
    return chatRepository.getMessage();
  } 
}

class NoParams {}