part of 'profile_bloc.dart';

sealed class ProfileEvent {}

// On Profile Update Event
final class ProfileUpdateEvent extends ProfileEvent {
  final String userId;
  final String name;
  String? token;
  File? avatar;

  ProfileUpdateEvent({
    required this.userId,
    required this.name,
    this.token,
    this.avatar,
  });
}

final class ProfileStopLoadingEvent extends ProfileEvent {}
