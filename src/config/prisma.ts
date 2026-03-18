import { env } from "./env.js";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";

const connectionString = env.dbUrl;

const adapter = new PrismaPg({
  connectionString,
});

const prisma = new PrismaClient({adapter});

export default prisma;