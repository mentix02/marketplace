import * as z from "zod";

const sellerSchema = z.object({
  name: z.string(),
  slug: z.string(),
  description: z.string().nullish(),
});
