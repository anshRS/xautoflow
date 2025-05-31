import 'package:client/bindings/dependencies.dart';
import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:client/features/auth/presentation/screens/login_screen.dart';
import 'package:client/features/chat/presentation/bloc/chat_bloc.dart';
import 'package:client/features/code/presentation/bloc/code_bloc.dart';
import 'package:client/features/home/presentation/screens/home_screen.dart';
import 'package:client/features/profile/presentation/bloc/profile_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load();
  await initDependencies();

  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => serviceLocator<AppUserCubit>()),
        BlocProvider(create: (_) => serviceLocator<AuthBloc>()),
        BlocProvider(create: (_) => serviceLocator<ProfileBloc>()),
        BlocProvider(create: (_) => serviceLocator<ChatBloc>()),
        BlocProvider(create: (_) => serviceLocator<CodeBloc>()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // This widget is the root of your application.
  @override
  void initState() {
    super.initState();
    context.read<AuthBloc>().add(AuthIsUserLoggedIn());
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'xAgent',
      home: BlocSelector<AppUserCubit, AppUserState, bool>(
        selector: (state) {   
          return state is AppUserLoggedIn;
        },
        builder: (context, state) {
          if (state) {
            return const HomeScreen();
          }
          return const LogInScreen();
        },
      ),
    );
  }
}
