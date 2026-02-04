"use client";

import * as z from "zod";
import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRef, useEffect, ComponentProps } from "react";
import { useForm, Controller, SubmitHandler } from "react-hook-form";

import { cn } from "@/lib/utils";
import { signIn, signUp } from "@/lib/auth-client";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, FieldError, FieldDescription, FieldGroup, FieldLabel, FieldSeparator } from "@/components/ui/field";

const signupFormSchema = z.object({
  name: z.string().nonempty("Your full name is required"),
  password: z.string().min(8, "Password must be at least 8 characters long"),
  email: z.email("Please enter a valid email address").nonempty("Your email is required"),
});

type SignupFormValues = z.infer<typeof signupFormSchema>;

export default function SignupForm({ className, ...props }: ComponentProps<"div">) {
  const nameRef = useRef<HTMLInputElement>(null);
  const {
    control,
    setError,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm({
    resolver: zodResolver(signupFormSchema),
    defaultValues: { name: "", email: "", password: "" },
  });

  // Autofocus the name input on mount
  useEffect(() => {
    nameRef.current?.focus();
  }, []);

  const handleGoogleSignUp = async () => {
    const { error } = await signIn.social({ provider: "google", callbackURL: "/" });
    if (error) setError("email", { message: error.message, type: error.statusText });
  };

  const onSubmit: SubmitHandler<SignupFormValues> = async (data) => {
    await signUp.email(
      { ...data, callbackURL: "/" },
      {
        onError: (ctx) => {
          setError("email", { message: ctx.error.message, type: ctx.error.statusText });
        },
      },
    );
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Create an Account</CardTitle>
          <CardDescription>Create your account to get started</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)}>
            <FieldGroup>
              <Field>
                <Button variant="outline" type="button" onClick={handleGoogleSignUp}>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path
                      d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                      fill="currentColor"
                    />
                  </svg>
                  Signup with Google
                </Button>
              </Field>

              <FieldSeparator className="*:data-[slot=field-separator-content]:bg-card">
                Or continue with
              </FieldSeparator>

              <Controller
                name="name"
                control={control}
                render={({ field, fieldState }) => (
                  <Field data-invalid={fieldState.invalid}>
                    <FieldLabel htmlFor="name">Name</FieldLabel>
                    <Input
                      {...field}
                      id="name"
                      ref={nameRef}
                      autoComplete="off"
                      placeholder="Your full name"
                      aria-invalid={fieldState.invalid}
                    />
                    {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                  </Field>
                )}
              />

              <Controller
                name="email"
                control={control}
                render={({ field, fieldState }) => (
                  <Field data-invalid={fieldState.invalid}>
                    <FieldLabel htmlFor="email">Email</FieldLabel>
                    <Input
                      {...field}
                      id="email"
                      autoComplete="off"
                      placeholder="email@provider.com"
                      aria-invalid={fieldState.invalid}
                    />
                    {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                  </Field>
                )}
              />

              <Controller
                name="password"
                control={control}
                render={({ field, fieldState }) => (
                  <Field data-invalid={fieldState.invalid}>
                    <FieldLabel htmlFor="password">Password</FieldLabel>
                    <Input
                      {...field}
                      type="password"
                      id="password"
                      placeholder="Create a password"
                      aria-invalid={fieldState.invalid}
                    />
                    {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                  </Field>
                )}
              />

              <Field>
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? <Spinner /> : "Sign Up"}
                </Button>
                <FieldDescription className="text-center">
                  Already have an account? <Link href="/sign-in">Log in</Link>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>

      <FieldDescription className="px-6 text-center">
        By signing up, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
      </FieldDescription>
    </div>
  );
}
