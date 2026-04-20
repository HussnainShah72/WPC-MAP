Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement the authentication module.

Pages and routes:
- /auth/login
- /auth/sign-up
- /auth/forgot-password

Requirements:
1. Email-based login using the custom User model
2. Login page must show:
   - title: Login
   - subtitle: Enter your email below to login to your account
   - fields: Email, Password
   - forgot password link
   - sign up link
   - button: Login
3. Invalid login must show:
   - "Invalid login credentials"
4. Signup page must show:
   - title: Sign up
   - subtitle: Create a new account
   - fields: Email, Password, Repeat Password
   - button: Sign up
5. Signup must only work if email exists in AllowedSignupEmail
6. If email is not approved, show:
   - "This email is not allowed to sign up"
7. On successful signup:
   - create User
   - copy role from AllowedSignupEmail
   - mark AllowedSignupEmail.is_registered = True
8. Forgot password page must show:
   - title: Reset Your Password
   - subtitle: Type in your email and we'll send you a link to reset your password
   - field: Email
   - button: Send reset email

Implementation notes:
- Use Django forms
- Use Django messages or inline error handling
- Keep templates visually clean and similar to the source app
- Add logout support if practical

After finishing:
- summarize changed files
- note any assumptions around password reset flow