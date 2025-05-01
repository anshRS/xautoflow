import 'package:client/common/usecases/usecase.dart';
import 'package:client/features/auth/domain/repositories/auth_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class UserSignUpUseCase implements UseCase<void, UserSignUpParams> {
  final AuthRepository authRepository;
  const UserSignUpUseCase(this.authRepository);

  @override
  Future<Either<Failure, void>> call(UserSignUpParams params) async {
    return await authRepository.signUpWithEmailPassword(
      name: params.name,
      email: params.email,
      password: params.password,
    );
  }
}

class UserSignUpParams {
  final String name;
  final String email;
  final String password;
  
  UserSignUpParams({
    required this.name,
    required this.email,
    required this.password,
  });
}