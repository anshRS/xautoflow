import 'package:client/features/code/domain/repositories/code_repository.dart';

class SendMessageUsecase {
  final CodeRepository codeRepository;

  const SendMessageUsecase(this.codeRepository);

  void call(SendMessageParams params) {
    return codeRepository.sendMessage(params.message);
  }
}

class SendMessageParams {
  final String message;

  SendMessageParams({
    required this.message
  });
}