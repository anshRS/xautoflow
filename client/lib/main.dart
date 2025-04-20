import 'package:flutter/material.dart';
import 'package:client/core/theme/app_theme.dart';
import 'package:client/features/dashboard/presentation/screens/dashboard_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'XAutoFlow',
      theme: AppTheme.lightTheme(),
      home: const DashboardScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
