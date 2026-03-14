import { PrismaClient } from '@prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import { Pool } from 'pg'
import { env } from '../config/env'

export const db = new Pool({
  host: env.dbHost,
  port: env.dbPort,
  user: env.dbUser,
  password: env.dbPassword,
  database: env.dbName,
  max: 20, 
  idleTimeoutMillis: 30000, 
  connectionTimeoutMillis: 2000,
});

db.on('error', (err) => {
  console.error('Erro inesperado no banco de dados', err);
  process.exit(-1);
});

const adapter = new PrismaPg(db as any)
const prisma = new PrismaClient()

export default prisma