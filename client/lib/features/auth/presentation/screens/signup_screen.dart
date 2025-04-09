import 'package:client/common/widgets/custom_button.dart';
import 'package:client/features/auth/presentation/widgets/auth_form_field.dart';
import 'package:flutter/material.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    nameController.dispose();
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
                  'assets/images/signup_image.png',
                  fit: BoxFit.cover,
                ),
              ),

              // Form Fields section
              Form(
                key: formKey,
                child: Flex(
                  direction: Axis.vertical,
                  spacing: 24,
                  children: [
                    Column(
                      children: [
                        Text(
                          "Create Account",
                          style: theme.textTheme.headlineLarge?.copyWith(
                            color: theme.colorScheme.onSurface,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "Create an account to explore features",
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
                          label: "Name",
                          hintText: "Enter you name",
                          isHidden: false,
                          icon: Icon(Icons.account_circle),
                          controller: nameController,
                        ),
                        AuthFormField(
                          label: "Email",
                          hintText: "Enter you email",
                          isHidden: false,
                          icon: Icon(Icons.email_outlined),
                          controller: emailController,
                        ),
                        AuthFormField(
                          label: "Password",
                          hintText: "Enter you password",
                          isHidden: true,
                          icon: Icon(Icons.lock_outline),
                          controller: passwordController,
                        ),
                      ],
                    ),

                    CustomButton(text: "Sign Up", onPressed: () {
                    }),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
