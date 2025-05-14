import 'dart:io';

import 'package:client/common/usecases/usecase.dart';
import 'package:client/features/profile/domain/entities/profile.dart';
import 'package:client/features/profile/domain/repository/profile_repository.dart';
import 'package:client/utils/error/failures.dart';
import 'package:fpdart/fpdart.dart';

class ProfileUpdateUsecase implements UseCase<Profile, ProfileUpdateParams> {
  final ProfileRepository profileRepository;
  const ProfileUpdateUsecase(this.profileRepository);

  @override
  Future<Either<Failure, Profile>> call(ProfileUpdateParams params) async {
    return await profileRepository.updateProfile(
      userId: params.userId,
      name: params.name,
      token: params.token,
      avatar: params.avatar,
    );
  }
}

class ProfileUpdateParams {
  final String userId;
  final String name;
  String? token;
  File? avatar;

  ProfileUpdateParams({
    required this.userId,
    required this.name,
    this.token,
    this.avatar,
  });
}
