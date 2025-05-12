import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:client/features/auth/presentation/screens/login_screen.dart';
import 'package:client/features/home/presentation/screens/home_screen.dart';
import 'package:client/features/home/presentation/widgets/custom_drawer_item.dart';
import 'package:client/features/profile/presentation/screens/profile_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CustomDrawer extends StatelessWidget {
  const CustomDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: SafeArea(
        child: SingleChildScrollView(
          child: BlocBuilder<AppUserCubit, AppUserState>(
            builder: (context, state) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.fromLTRB(28, 16, 16, 10),
                    child: Text(
                      (state is AppUserLoggedIn) ? state.user.name : "",
                    ),
                  ),
                  CustomDrawerItem(
                    label: 'Features',
                    icon: Icons.file_open_outlined,
                    onTap: () {
                      Navigator.push(context, HomeScreen.route());
                    },
                  ),
                  CustomDrawerItem(
                    label: 'Profile',
                    icon: Icons.settings_outlined,
                    onTap: () {
                      Navigator.push(context, ProfileScreen.route());
                    },
                  ),
                  CustomDrawerItem(
                    label: 'Logout',
                    icon: Icons.logout,
                    onTap: () {
                      context.read<AuthBloc>().add(AuthLogoutEvent());
                      Navigator.pushAndRemoveUntil(
                        context,
                        LogInScreen.route(),
                        (route) => false,
                      );
                    },
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
}
