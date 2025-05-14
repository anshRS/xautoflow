import 'dart:io';

import 'package:client/features/profile/domain/entities/profile.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

abstract interface class ProfileRepository {
  Future<Either<Failure, Profile>> updateProfile({
    required String userId,
    required String name,
    String? token,
    File? avatar,
  });
}