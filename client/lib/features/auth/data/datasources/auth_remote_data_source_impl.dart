import 'package:client/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:client/features/auth/data/models/user_model.dart';
import 'package:client/utils/http/http_client.dart';

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {

  AuthRemoteDataSourceImpl();

  @override
  Future<void> signUpWithEmailPassword({
    required String name,
    required String email,
    required String password,
  }) async {
    try { 
      await HttpHelper.post('auth/register', {
        'name': name,
        'email': email,
        'password': password,
      });
    } catch (e) {
      rethrow; 
    }
  }

  @override
  Future<UserModel> loginWithEmailPassword({
    required String email,
    required String password,
  }) async {
    try {
      final response = await HttpHelper.post('auth/login', {
        'email': email,
        'password': password,
      });

      return UserModel.fromJson(response!["data"]);
    } catch (e) {
      rethrow;
    }
  }
  
  @override
  Future<UserModel> getCurrentUser(String token) async {
    try {
      final response = await HttpHelper.get(
        'auth',
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        }
      );
      
      return UserModel.fromJson(response!["data"]).copyWith(
        token: token,
      );
    } catch (e) {
      rethrow;      
    }    
  }
}
