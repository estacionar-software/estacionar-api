import { app } from './app';

const start = async () => {
  try {
    await app.listen({ port: 8080, host: '0.0.0.0' });
    console.log('Servidor rodando em http://localhost:8080');
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();