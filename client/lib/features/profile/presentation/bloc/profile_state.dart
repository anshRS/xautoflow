part of 'profile_bloc.dart';

@immutable
sealed class ProfileState {
  const ProfileState();
}

final class ProfileInitial extends ProfileState {}

// Loading States
final class ProfileLoadingState extends ProfileState {}
final class ProfileStopLoadingState extends ProfileState {}

// Error States
final class ProfileFailureState extends ProfileState {
  final String message;
  const ProfileFailureState(this.message);
}

// Success States
final class ProfileUpdateSuccessState extends ProfileState {
  final Profile profile;
  const ProfileUpdateSuccessState(this.profile);
}