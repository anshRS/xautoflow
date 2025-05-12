import 'package:client/common/entities/user.dart';
import 'package:client/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:client/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:client/features/auth/domain/repositories/auth_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;

  AuthRepositoryImpl(this.remoteDataSource, this.localDataSource);

  @override
  Future<Either<Failure, void>> signUpWithEmailPassword({
    required String name,
    required String email,
    required String password,
  }) async {
    try {
      await remoteDataSource.signUpWithEmailPassword(
        name: name,
        email: email,
        password: password,
      );
      return right(null);
    } catch (e) {
      return left(Failure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> loginWithEmailPassword({
    required String email,
    required String password,
  }) async {
    try {
      final data = await remoteDataSource.loginWithEmailPassword(
        email: email,
        password: password,
      );
      await localDataSource.saveToken(data.token);
      return right(data);
    } catch (e) {
      return left(Failure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    try {
      final token = await localDataSource.getToken();

      if (token == null) {
        return left(Failure("Invalid access"));
      }

      final data = await remoteDataSource.getCurrentUser(token);

      return right(data);
    } catch (e) {
      return left(Failure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> logoutUser() async {
    try {
      await localDataSource.clearToken();
      return right(null);
    } catch (e) {
      return left(Failure(e.toString()));
    }
  }
}
