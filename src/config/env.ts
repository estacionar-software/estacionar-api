import 'dotenv/config';

export const env = {
  dbHost: process.env.DB_HOST || '127.0.0.1',
  dbPort: Number(process.env.DB_PORT) || 5432,
  dbUser: process.env.DB_USER || 'postgres',
  dbPassword: process.env.DB_PASSWORD || '',
  dbName: process.env.DB_NAME || 'postgres',
  port: Number(process.env.PORT) || 3000,
};