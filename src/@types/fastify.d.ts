import "@fastify/jwt";

declare module "fastify" {
    interface FastifyRequest {
        user: {
            id: string;
            name: string;
            email: string;
            role: string;
            createdAt: Date;
        };
    }
}