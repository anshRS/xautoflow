
import 'package:client/features/code/domain/repositories/code_repository.dart';

class ConnectCodeUsecase {
  final CodeRepository coderepository;

  ConnectCodeUsecase(this.coderepository);

  Future<void> call(ConnectParams params) {
    return coderepository.connect(params.userId);
  }
}

class ConnectParams {
  final String userId;

  ConnectParams({required this.userId});
}