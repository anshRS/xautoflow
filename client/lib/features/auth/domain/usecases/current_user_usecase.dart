import 'package:client/common/entities/user.dart';
import 'package:client/common/usecases/usecase.dart';
import 'package:client/features/auth/domain/repositories/auth_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class GetCurrentUserUsecase implements UseCase<User, NoParams> {
  final AuthRepository authRepository;
  GetCurrentUserUsecase(this.authRepository);

  @override
  Future<Either<Failure, User>> call(NoParams params) async {
    return await authRepository.getCurrentUser();
  }  
}