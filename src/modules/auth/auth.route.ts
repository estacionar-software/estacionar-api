import { FastifyInstance } from "fastify";
import { AuthController } from "./auth.controller";

export async function AuthRoutes(app: FastifyInstance) {
    app.post("/     ", {
        schema: {
            body: {
                type: "object",
                properties: {
                    licensePlate: { type: "string" },
                    model: { type: "string" },
                    locale: { type: "string" },
                },
                required: ["licensePlate", "model", "locale"],
            },
        },
    }, AuthController);
}
