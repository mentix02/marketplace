import * as z from "zod";
import { createFetch, createSchema, FetchSchemaRoutes } from "@better-fetch/fetch";

import { getBearerToken } from "@/lib/auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

const skeyParamSchema = z.object({ skey: z.uuidv4() }).readonly();
const slugParamSchema = z.object({ slug: z.string() }).readonly();

const publicSchemaRoutes = {
  "@get/api/": {},
} as const satisfies FetchSchemaRoutes;

const privateSchemaRoutes = {} as const satisfies FetchSchemaRoutes;

const publicFetchSchema = createSchema({ ...publicSchemaRoutes }, { strict: true });

const privateFetchSchema = createSchema({ ...publicSchemaRoutes, ...privateSchemaRoutes }, { strict: true });

export const $publicFetch = createFetch({
  baseURL: BASE_URL,
  schema: publicFetchSchema,
});

export const $privateFetch = createFetch({
  baseURL: BASE_URL,
  schema: privateFetchSchema,
  auth: { type: "Bearer", token: getBearerToken },
});
