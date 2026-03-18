import { FastifyInstance } from "fastify";
import { AuthController } from "./auth.controller.js";

export async function AuthRoutes(app: FastifyInstance) {
    app.post("/tenant", {
        schema: {
            body: {
                type: "object",
                properties: {
                    tenantData: {
                        type: "object",
                        properties: {
                            businessName: { type: "string" },
                            document: { type: "string" },
                        },
                        required: ["businessName", "document"],
                    },
                    adminData: {
                        type: "object",
                        properties: {
                            name: { type: "string" },
                            email: { type: "string" },
                            password: { type: "string" },
                    },
                    required: ["name", "email", "password"],
                }
                },
                required: ["tenantData", "adminData"],
            },
        },
    }, AuthController);
}
