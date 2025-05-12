import 'package:client/common/widgets/custom_button.dart';
import 'package:client/common/widgets/custom_snackbar.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:client/features/home/presentation/screens/home_screen.dart';
import 'package:client/features/auth/presentation/screens/signup_screen.dart';
import 'package:client/features/auth/presentation/widgets/auth_form_field.dart';
import 'package:client/utils/validators/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LogInScreen extends StatefulWidget {
  static route() =>
      MaterialPageRoute(builder: (context) => const LogInScreen());
  const LogInScreen({super.key});

  @override
  State<LogInScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<LogInScreen> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Flex(
            direction: Axis.vertical,
            children: [
              // Image section
              SizedBox(
                height: 460,
                child: Image.asset(
                  'assets/images/login_image.png',
                  fit: BoxFit.cover,
                ),
              ),

              // Form Fields section
              BlocConsumer<AuthBloc, AuthState>(
                listener: (context, state) {
                  if (state is AuthFailureState) {
                    CustomPopUp.errorSnackBar(
                      context: context,
                      message: state.message,
                    );
                  }

                  if (state is AuthLoginSuccessState) {
                    context.read<AuthBloc>().add(AuthStopLoadingEvent());
                    Navigator.pushAndRemoveUntil(
                      context,
                      HomeScreen.route(),
                      (route) => false,
                    );
                  }
                },
                builder: (context, state) {
                  return Form(
                    key: formKey,
                    child: Flex(
                      direction: Axis.vertical,
                      spacing: 24,
                      children: [
                        Column(
                          children: [
                            Text(
                              "Login",
                              style: theme.textTheme.headlineLarge?.copyWith(
                                color: theme.colorScheme.onSurface,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              "Welcome back you've been missed!",
                              style: theme.textTheme.bodyLarge?.copyWith(
                                color: theme.colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ),

                        Flex(
                          direction: Axis.vertical,
                          spacing: 16,
                          children: [
                            AuthFormField(
                              label: "Email",
                              hintText: "Enter you email",
                              isHidden: false,
                              icon: Icon(Icons.email_outlined),
                              controller: emailController,
                              validator:
                                  (value) => Validator.validateEmail(value),
                            ),
                            AuthFormField(
                              label: "Password",
                              hintText: "Enter you password",
                              isHidden: true,
                              icon: Icon(Icons.lock_outline),
                              controller: passwordController,
                              validator:
                                  (value) => Validator.validateEmptyField(
                                    'Password',
                                    value,
                                  ),
                            ),
                          ],
                        ),

                        CustomButton(
                          text: "Login",
                          onPressed: () {
                            if (formKey.currentState!.validate()) {
                              context.read<AuthBloc>().add(
                                AuthLoginEvent(
                                  email: emailController.text.trim(),
                                  password: passwordController.text.trim(),
                                ),
                              );
                            }
                          },
                          loading: (state is AuthLoadingState) ? true : false,
                        ),
                      ],
                    ),
                  );
                },
              ),
              const SizedBox(height: 8),
              GestureDetector(
                onTap: () {
                  Navigator.push(context, SignUpScreen.route());
                },
                child: Text.rich(
                  TextSpan(
                    children: [
                      TextSpan(
                        text: "Don't have account? ",
                        style: theme.textTheme.bodyLarge?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                      ),
                      TextSpan(
                        text: "Create now",
                        style: theme.textTheme.bodyLarge?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
