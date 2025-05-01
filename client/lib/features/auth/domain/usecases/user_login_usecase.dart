import 'package:client/common/entities/user.dart';
import 'package:client/common/usecases/usecase.dart';
import 'package:client/features/auth/domain/repositories/auth_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class UserLoginUseCase implements UseCase<User, UserLoginParams> {
  final AuthRepository authRepository;
  const UserLoginUseCase(this.authRepository);

  @override
  Future<Either<Failure, User>> call(UserLoginParams params) async {
    return await authRepository.loginWithEmailPassword(
      email: params.email,
      password: params.password,
    );
  }
}

class UserLoginParams {
  final String email;
  final String password;

  UserLoginParams({
    required this.email,
    required this.password,
  });
}