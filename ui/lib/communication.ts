import type { User } from "better-auth";

interface SendMailArgs {
  user: User;
  url: string;
}

const sendEmail = async (to: string, subject: string, body: string) => {
  // Simulate sending an email.
  // Implement your own email sending logic here. You can use something like nodemailer.
  console.log("===============================");
  console.log(`Sending email to: ${to}`);
  console.log(`Subject: ${subject}`);
  console.log(`Body: ${body}`);
  console.log("===============================");
  return Promise.resolve(true);
};

export const sendVerificationEmail = async ({ user, url }: SendMailArgs) =>
  void (await sendEmail(user.email, "Verify your email", `Click here to verify your email: ${url}`));

export const sendResetPasswordEmail = async ({ user, url }: SendMailArgs) =>
  void (await sendEmail(user.email, "Reset your password", `Click here to reset your password: ${url}`));

export default sendEmail;
