import 'package:client/features/auth/data/models/user_model.dart';

abstract interface class AuthRemoteDataSource {
  Future<void> signUpWithEmailPassword({
    required String name,
    required String email,
    required String password,
  });

  Future<UserModel> loginWithEmailPassword({
    required String email,
    required String password,
  });

  Future<UserModel> getCurrentUser(String token);
}
