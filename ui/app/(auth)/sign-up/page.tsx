import type { Metadata } from "next";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { Paintbrush2 } from "lucide-react";

import { auth } from "@/lib/auth";
import SignupForm from "@/components/auth/signup-form";

export const metadata: Metadata = {
  title: "Sign Up",
  description: "Create a new account",
};

export default async function Page() {
  const session = await auth.api.getSession({ headers: await headers() });

  if (session) redirect("/");

  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <a href="/" className="flex items-center gap-2 self-center font-medium">
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <Paintbrush2 className="size-4" />
          </div>
          Karigari
        </a>
        <SignupForm />
      </div>
    </div>
  );
}
