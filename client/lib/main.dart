import 'package:client/bindings/dependencies.dart';
import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:client/features/auth/presentation/screens/login_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  initDependencies();

  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => serviceLocator<AppUserCubit>()),
        BlocProvider(create: (_) => serviceLocator<AuthBloc>()),
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
            return const Scaffold(body: Center(child: Text('Logged in!')));
          }
          return const LogInScreen();
        },
      ),
    );
  }
}
