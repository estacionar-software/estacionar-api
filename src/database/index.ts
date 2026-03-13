import { Pool } from 'pg';
import { env } from '../config/env';

export const db = new Pool({
  host: env.dbHost,
  port: env.dbPort,
  user: env.dbUser,
  password: env.dbPassword,
  database: env.dbName,
  
  max: 20, //máximo de clientes no pool
  idleTimeoutMillis: 30000, //tempo máximo que uma conexão pode ficar ociosa
  connectionTimeoutMillis: 2000, //tempo máximo para tentar conectar
});

db.on('error', (err) => {
  console.error('Erro inesperado no banco de dados', err);
  process.exit(-1);
});