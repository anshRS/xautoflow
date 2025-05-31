import 'package:client/features/code/domain/repositories/code_repository.dart';

class DisconnectCodeUsecase {
  final CodeRepository codeRepository;

  const DisconnectCodeUsecase(this.codeRepository);

  void call() {
    codeRepository.disconnect();
  }

}