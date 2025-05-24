import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/widgets/animated_navigation.dart';
import 'package:client/features/chat/presentation/screens/chat_screen.dart';
import 'package:client/features/home/presentation/widgets/agent.dart';
import 'package:client/features/profile/presentation/screens/profile_screen.dart';
import 'package:client/features/home/presentation/widgets/custom_drawer.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class HomeScreen extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => const HomeScreen());
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      drawer: CustomDrawer(),
      appBar: AppBar(
        leading: Builder(
          builder: (context) {
            return IconButton(
              onPressed: () => Scaffold.of(context).openDrawer(),
              icon: Icon(Icons.menu),
            );
          },
        ),
        actions: [
          BlocBuilder<AppUserCubit, AppUserState>(
            builder: (context, state) {
              Widget avatarWidget;

              if (state is AppUserLoggedIn && state.user.avatarUrl.isNotEmpty) {
                avatarWidget = CircleAvatar(
                  backgroundImage: NetworkImage(state.user.avatarUrl),
                  backgroundColor: Colors.transparent,
                );
              } else if (state is AppUserLoggedIn) {
                avatarWidget = CircleAvatar(
                  backgroundColor: Colors.blueGrey,
                  child: Text(
                    state.user.name[0].toUpperCase(),
                    style: TextStyle(color: Colors.white),
                  ),
                );
              } else {
                avatarWidget = Icon(Icons.account_circle);
              }

              return IconButton(
                onPressed: () {
                  Navigator.push(context, ProfileScreen.route());
                },
                icon: avatarWidget,
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          BlocBuilder<AppUserCubit, AppUserState>(
            builder: (context, state) {
              return Container(
                color: theme.colorScheme.surfaceContainerLow,
                height: MediaQuery.of(context).size.height * 0.4,
                width: double.infinity,
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      (state is AppUserLoggedIn) ? state.user.name : " ",
                      style: theme.textTheme.displayLarge?.copyWith(
                        color: theme.colorScheme.onSurface,
                      ),
                    ),
                    Text(
                      "Welcome Back!",
                      style: theme.textTheme.titleLarge?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
          const SizedBox(height: 16),
          Text(
            "Features",
            style: theme.textTheme.titleLarge?.copyWith(
              color: theme.colorScheme.onSurface,
            ),
          ),
          const SizedBox(height: 16),
          Expanded(
            child: GridView.count(
              crossAxisCount: 2,
              crossAxisSpacing: 8,
              mainAxisSpacing: 8,
              padding: EdgeInsets.symmetric(horizontal: 8),
              children: [
                Agent(
                  agentName: "RealTime Chat",
                  icon: Icon(Icons.smart_toy_outlined),
                  description: "Facilitates instant, dynamic conversations",
                  onTap: () {
                    Navigator.push(context, bounceSlideUpRoute(const ChatScreen()));
                  },
                ),
                Agent(
                  agentName: "Finance",
                  icon: Icon(Icons.query_stats),
                  description:
                      "Smart financial insights and analysis for better decisions",
                  onTap: () {},
                ),
                Agent(
                  agentName: "Emailing",
                  icon: Icon(Icons.email_outlined),
                  description: "Automated email for seamless communication",
                  onTap: () {},
                ),
                Agent(
                  agentName: "Coding",
                  icon: Icon(Icons.code),
                  description: "Intelligent code generation faster development",
                  onTap: () {},
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
