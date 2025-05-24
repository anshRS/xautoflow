import 'dart:io';

import 'package:client/features/profile/data/datasources/profile_remote_data_source.dart';
import 'package:client/features/profile/data/models/profile_model.dart';
import 'package:client/utils/http/http_client.dart';

class ProfileRemoteDataSourceImpl implements ProfileRemoteDataSource {
  @override
  Future<ProfileModel> updateProfile({
    required String userId,
    required String name,
    String? token,
    File? avatar,
  }) async {
    try {
      final response = await HttpHelper.multipartPost(
        'profile/',
        fields: {'user_id': userId, 'name': name},
        file: avatar,
        headers: {'Authorization': 'Bearer $token'},
      );     

      return ProfileModel.fromJson(response!["data"][0]);
    } catch (e) {
      rethrow;
    }
  }
}
