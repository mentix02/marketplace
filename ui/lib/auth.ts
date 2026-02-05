import { redis } from "bun";
import * as crypto from "crypto";

import { eq } from "drizzle-orm";
import { createAuthMiddleware } from "better-auth/api";
import { betterAuth, BetterAuthOptions } from "better-auth";
// Plugins
import { admin } from "better-auth/plugins";
import { nextCookies } from "better-auth/next-js";
import { jwt, customSession } from "better-auth/plugins";

import { sendVerificationEmail, sendResetPasswordEmail } from "@/lib/communication";
import db, { pgPool, userTable, hashPassword, verifyPassword } from "@/lib/database";

const betterAuthOptions = {
  // Storages
  database: pgPool,
  advanced: { database: { generateId: "serial" } },
  // Uncomment the secondaryStorage object and the redis import at the top
  // to use an in-memory storage for faster session management. Note: some
  // migrations with the BetterAuth CLI tool may not work because Bun doesn't support
  // better-sqlite - and the CLI needs it. It's dumb, I know. To generate schemas
  // and process the migrations, just uncomment the Bun import and the secondaryStorage.

  secondaryStorage: {
    get: async (key: string) => await redis.get(key),
    delete: async (key: string) => void (await redis.del(key)),
    set: async (key: string, value: string, ttl?: number) =>
      await (ttl ? redis.set(key, value, "EX", ttl) : redis.set(key, value)),
  },

  // Social Providers
  // Uncomment and configure the providers you want to use.
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  // Plugins
  plugins: [
    admin({
      schema: {
        user: {
          fields: {
            banReason: "ban_reason",
            banExpires: "ban_expires",
          },
        },
      },
    }),
    jwt({
      jwks: { keyPairConfig: { alg: "RS256" } },
      schema: { jwks: { modelName: "better_auth_jwk" } },
      jwt: {
        definePayload: ({ user }) => ({
          user_id: user.id,
          token_type: "access",
          // Really important for drf-simplejwt
          jti: crypto.randomUUID().replace(/-/g, ""),
        }),
      },
    }),
    nextCookies(),
  ],
  // Email Verification
  emailVerification: {
    sendOnSignIn: true,
    sendOnSignUp: true,
    sendVerificationEmail: sendVerificationEmail,
  },
  // Email & password configuration.
  hooks: {
    after: createAuthMiddleware(async (ctx) => {
      // Set last_login after a successful sign-in
      if (ctx.path !== "/sign-in/email" && ctx.path !== "/callback/:id") return;
      const context = ctx.context;

      if (context.newSession?.user)
        await db
          .update(userTable)
          .set({ last_login: new Date() })
          .where(eq(userTable.id, parseInt(context.newSession.user.id)));
    }),
  },
  databaseHooks: {
    user: {
      create: {
        before: async (user, context) => {
          if (!context || !context.body || !context.body.password) return { data: user };

          const hashedPassword = await context?.context.password.hash(context.body.password);
          const userWithPassword = { ...user, password: hashedPassword };
          return { data: userWithPassword };
        },
      },
    },
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendResetPassword: sendResetPasswordEmail,
    password: { hash: hashPassword, verify: verifyPassword },
  },
  // Session management
  session: {
    modelName: "better_auth_session",
    cookieCache: { enabled: true, maxAge: 5 * 60 }, // 5 minutes
  },

  // Core database schema config.
  account: { modelName: "better_auth_account", accountLinking: { enabled: true } },
  verification: { modelName: "better_auth_verification" },
  user: {
    modelName: "user_user", // Django naming convention: appName_modelName
    fields: {
      updatedAt: "updated_at",
      createdAt: "date_joined",
      emailVerified: "email_verified",
    },
    additionalFields: {
      last_login: { type: "date", required: false, input: false },
      password: { type: "string", required: false, input: false, defaultValue: "" },
      is_staff: { type: "boolean", defaultValue: false, required: true, input: false },
      is_active: { type: "boolean", defaultValue: true, required: true, input: false },
      is_superuser: { type: "boolean", defaultValue: false, required: true, input: false },
    },
  },
} satisfies BetterAuthOptions;

export const auth = betterAuth({
  ...betterAuthOptions,
  plugins: [
    // Customise the session to omit the password field.
    // Sorry for this fuckery but this is the recommended approach by BetterAuth.
    ...(betterAuthOptions.plugins ?? []),
    customSession(async ({ user, session }) => {
      const { password, ...userWithoutPassword } = user;
      return { user: userWithoutPassword, session };
    }, betterAuthOptions),
  ],
});

export type Session = typeof auth.$Infer.Session;
