import 'dart:io';

import 'package:client/features/profile/data/models/profile_model.dart';

abstract interface class ProfileRemoteDataSource {
  Future<ProfileModel> updateProfile({
    required String userId,
    required String name,
    String? token,
    File? avatar,
  });
}