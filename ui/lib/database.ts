import { Pool } from "pg";
import { drizzle } from "drizzle-orm/node-postgres";
import { text, varchar, bigint, pgTable, boolean, timestamp } from "drizzle-orm/pg-core";

export const pgPool = new Pool({ connectionString: process.env.DATABASE_URL });

const DJ_ARGON_PREFIX = "argon2";
const db = drizzle({ client: pgPool });

export const userTable = pgTable("user_user", {
  image: text(),
  name: varchar({ length: 255 }).notNull(),
  email: varchar({ length: 254 }).notNull(),
  password: varchar({ length: 128 }).notNull().default(""),

  is_staff: boolean().notNull().default(false),
  is_active: boolean().notNull().default(true),
  is_superuser: boolean().notNull().default(false),
  email_verified: boolean()
    .$default(() => false)
    .notNull(),

  last_login: timestamp({ withTimezone: true }),
  updated_at: timestamp({ withTimezone: true })
    .$onUpdate(() => new Date())
    .notNull(),
  date_joined: timestamp({ withTimezone: true })
    .notNull()
    .$default(() => new Date()),

  access_key: varchar({ length: 32 }).notNull(),
  id: bigint({ mode: "number" }).primaryKey().generatedByDefaultAsIdentity(),
});

export default db;

export const hashPassword = async (password: string) =>
  DJ_ARGON_PREFIX + (await Bun.password.hash(password, { timeCost: 2, memoryCost: 102400, algorithm: "argon2id" }));

interface VerifyPasswordArgs {
  hash: string;
  password: string;
}

export const verifyPassword = async ({ hash, password }: VerifyPasswordArgs): Promise<boolean> =>
  await Bun.password.verify(
    password,
    hash.startsWith(DJ_ARGON_PREFIX) ? hash.substring(DJ_ARGON_PREFIX.length) : hash,
    "argon2id",
  );
