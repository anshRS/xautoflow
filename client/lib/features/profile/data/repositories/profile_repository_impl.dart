import 'dart:io';

import 'package:client/features/profile/data/datasources/profile_remote_data_source.dart';
import 'package:client/features/profile/domain/entities/profile.dart';
import 'package:client/features/profile/domain/repository/profile_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class ProfileRepositoryImpl implements ProfileRepository {
  final ProfileRemoteDataSource remoteDataSource;

  ProfileRepositoryImpl(this.remoteDataSource);

  @override
  Future<Either<Failure, Profile>> updateProfile({
    required String userId,
    required String name,
    String? token,
    File? avatar,
  }) async {
    try {
      final data = await remoteDataSource.updateProfile(
        userId: userId,
        name: name,
        token: token,
        avatar: avatar,
      );

      return right(data);
    } catch (e) {
      return left(Failure(e.toString()));
    }
  }
}
