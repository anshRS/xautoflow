import 'dart:io';

import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/entities/user.dart';
import 'package:client/features/profile/domain/entities/profile.dart';
import 'package:client/features/profile/domain/usecases/profile_update_usecase.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'profile_event.dart';
part 'profile_state.dart';

class ProfileBloc extends Bloc<ProfileEvent, ProfileState> {
  final ProfileUpdateUsecase _profileUpdateUsecase;
  final AppUserCubit _appUserCubit;

  ProfileBloc({
    required ProfileUpdateUsecase profileUpdateUsecase,
    required AppUserCubit appUserCubit,
  }) : _profileUpdateUsecase = profileUpdateUsecase,
       _appUserCubit = appUserCubit,
       super(ProfileInitial()) {
    on<ProfileUpdateEvent>(_onProfileUpdateEvent);
    on<ProfileStopLoadingEvent>(_onProfileStopLoadingEvent);
  }

  void _onProfileUpdateEvent(
    ProfileUpdateEvent event,
    Emitter<ProfileState> emit,
  ) async {
    emit(ProfileLoadingState());

    final res = await _profileUpdateUsecase(
      ProfileUpdateParams(
        userId: event.userId,
        name: event.name,
        token: event.token,
        avatar: event.avatar,
      ),
    );

    res.fold(
      (l) => emit(ProfileFailureState(l.message)),
      (r) {
        emit(ProfileUpdateSuccessState(r));

        // Get current app user
        final currentUserState = _appUserCubit.state;
        if(currentUserState is AppUserLoggedIn) {
          final updatedUser = User(
            id: r.id,
            name: r.name,
            email: r.email,
            avatarUrl: r.avatarUrl,
            token: currentUserState.user.token,
          );

          // Update app-wide user
          _appUserCubit.updateUser(updatedUser);
        }

      });    
  }

  _onProfileStopLoadingEvent(ProfileStopLoadingEvent event, Emitter<ProfileState> emit) {
    emit(ProfileStopLoadingState());
  }
}
