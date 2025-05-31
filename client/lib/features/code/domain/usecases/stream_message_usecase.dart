import 'package:client/common/entities/message.dart';
import 'package:client/features/code/domain/repositories/code_repository.dart';

class StreamMessageUsecase {
  final CodeRepository codeRepository;

  const StreamMessageUsecase(this.codeRepository);

  Stream<MessageEntity> call(NoParams params) {
    return codeRepository.getMessage();
  } 
}

class NoParams {}