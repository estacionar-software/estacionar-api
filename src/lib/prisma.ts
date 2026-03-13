import { PrismaClient } from '@prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import { Pool } from 'pg'
import {env} from '../config/env'

const pool = new Pool({ connectionString: env.dbHost })
const adapter = new PrismaPg(pool as any)
const prisma = new PrismaClient({ adapter })

export default prisma