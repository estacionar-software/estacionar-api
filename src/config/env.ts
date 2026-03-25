import 'dotenv/config';

export const env = {
  dbHost: process.env.DB_HOST || '127.0.0.1',
  dbPort: Number(process.env.DB_PORT) || 5433,
  dbUser: process.env.DB_USER || 'admin',
  dbPassword: process.env.DB_PASSWORD || 'estacionar123',
  dbName: process.env.DB_NAME || 'estacionar-db',
  port: Number(process.env.PORT) || 3000,
  dbUrl: process.env.DATABASE_URL || 'postgresql://${env.dbUser}:${env.dbPassword}@${env.dbHost}:${env.dbPort}/${env.dbName}?schema=public',
  jwtSecret: process.env.JWT_SECRET,
};