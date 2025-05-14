import 'dart:io';

import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/widgets/custom_button.dart';
import 'package:client/common/widgets/custom_snackbar.dart';
import 'package:client/features/profile/presentation/bloc/profile_bloc.dart';
import 'package:client/features/profile/presentation/widgets/profile_form_field.dart';
import 'package:client/utils/device/device_utility.dart';
import 'package:client/utils/validators/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ProfileScreen extends StatefulWidget {
  static route() =>
      MaterialPageRoute(builder: (context) => const ProfileScreen());
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  late final TextEditingController nameController;
  late final TextEditingController emailController;
  final formKey = GlobalKey<FormState>();
  File? image;

  void selectProfileImage() async {
    final pickedImage = await DeviceUtils.pickImage();
    if (pickedImage != null) {
      setState(() {
        image = pickedImage;
      });
    }
  }

  void updateProfile() {
    if (formKey.currentState!.validate()) {
      final user = (context.read<AppUserCubit>().state as AppUserLoggedIn).user;
      context.read<ProfileBloc>().add(
        ProfileUpdateEvent(
          userId: user.id,
          name: nameController.text.trim(),
          token: user.token,
          avatar: image,
        ),
      );
    }
  }

  @override
  void initState() {
    super.initState();

    final userState = context.read<AppUserCubit>().state;
    if (userState is AppUserLoggedIn) {
      nameController = TextEditingController(text: userState.user.name);
      emailController = TextEditingController(text: userState.user.email);
    } else {
      nameController = TextEditingController();
      emailController = TextEditingController();
    }
  }

  @override
  void dispose() {
    nameController.dispose();
    emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Profile',
          style: theme.textTheme.titleLarge?.copyWith(
            color: theme.colorScheme.onSurface,
          ),
        ),
      ),
      body: BlocConsumer<ProfileBloc, ProfileState>(
        listener: (context, state) {
          if (state is ProfileFailureState) {
            CustomPopUp.errorSnackBar(context: context, message: state.message);
          }

          if (state is ProfileUpdateSuccessState) {
            CustomPopUp.successSnackBar(
              context: context,
              message: "Profile Updated!",
            );
            context.read<ProfileBloc>().add(ProfileStopLoadingEvent());
          }
        },
        builder: (context, state) {
          return SingleChildScrollView(
            child: Form(
              key: formKey,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Flex(
                  direction: Axis.vertical,
                  spacing: 32,
                  children: [
                    BlocBuilder<AppUserCubit, AppUserState>(
                      builder: (context, state) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 64),
                          child: GestureDetector(
                            onTap: () {
                              selectProfileImage();
                            },
                            child: Container(
                              width: 182,
                              height: 182,
                              decoration: BoxDecoration(shape: BoxShape.circle),
                              child: Stack(
                                children: [
                                  // Avatar background (icon instead of image)
                                  Positioned.fill(
                                    child: CircleAvatar(
                                      child:
                                          image != null
                                              ? GestureDetector(
                                                onTap: selectProfileImage,
                                                child: Container(
                                                  width: 160,
                                                  height: 160,
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                  ),

                                                  child: ClipRRect(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                          80,
                                                        ),
                                                    child: Image.file(
                                                      image!,
                                                      fit: BoxFit.cover,
                                                    ),
                                                  ),
                                                ),
                                              )
                                              : (state is AppUserLoggedIn &&
                                                  state
                                                      .user
                                                      .avatarUrl
                                                      .isNotEmpty)
                                              ? ClipOval(
                                                child: Image.network(
                                                  state.user.avatarUrl,
                                                  fit: BoxFit.cover,
                                                  width: 160,
                                                  height: 160,
                                                  errorBuilder: (
                                                    context,
                                                    error,
                                                    stackTrace,
                                                  ) {
                                                    return Center(
                                                      child: Text(
                                                        state.user.name[0]
                                                            .toUpperCase(),
                                                        style: const TextStyle(
                                                          fontSize: 91,
                                                        ),
                                                      ),
                                                    );
                                                  },
                                                ),
                                              )
                                              : Center(
                                                child: Text(
                                                  (state is AppUserLoggedIn)
                                                      ? state.user.name[0]
                                                          .toUpperCase()
                                                      : "",
                                                  style: const TextStyle(
                                                    fontSize: 91,
                                                  ),
                                                ),
                                              ),
                                    ),
                                  ),

                                  // Camera button at bottom-right
                                  Positioned(
                                    bottom: 12,
                                    right: 12,
                                    child: Container(
                                      padding: const EdgeInsets.all(6),
                                      decoration: BoxDecoration(
                                        shape: BoxShape.circle,
                                        color: theme.colorScheme.primary,
                                      ),
                                      child: Icon(
                                        Icons.camera_alt,
                                        size: 20,
                                        color: theme.colorScheme.onPrimary,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                    Flex(
                      direction: Axis.vertical,
                      spacing: 16,
                      children: [
                        ProfileFormField(
                          label: "Name",
                          hintText: "Enter you name",
                          icon: Icon(Icons.account_circle),
                          controller: nameController,
                          validator:
                              (value) =>
                                  Validator.validateEmptyField('Name', value),
                          enabled: true,
                        ),

                        ProfileFormField(
                          label: "Email",
                          hintText: "Enter you email",
                          icon: Icon(Icons.email_outlined),
                          controller: emailController,
                          enabled: false,
                        ),
                      ],
                    ),
                    CustomButton(
                      text: "Update Profile",
                      onPressed: () {
                        updateProfile();
                      },
                      loading: (state is ProfileLoadingState) ? true : false,
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
