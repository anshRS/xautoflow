import 'package:client/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final SharedPreferences prefs;
  static const _tokenKey = 'ACCESS_TOKEN';

  AuthLocalDataSourceImpl(this.prefs);
  
  @override
  Future<void> saveToken(String token) async {
    await prefs.setString(_tokenKey, token);
  }

  @override
  Future<String?> getToken() async {
    return prefs.getString(_tokenKey);
  }

  @override
  Future<void> clearToken() async {
    await prefs.remove(_tokenKey);
  }
}
