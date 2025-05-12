class User {
  final String id;
  final String name;
  final String email;
  final String avatarUrl;
  final String token;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.avatarUrl,
    required this.token,
  });

  @override
  String toString() {
    return 'User(id: $id, name: $name, email: $email, avatarUrl: $avatarUrl, token: $token)';
  }
}
