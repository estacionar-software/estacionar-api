import { FastifyInstance } from "fastify";
import { createVehicleController } from "./vehicles.controller";

export async function vehiclesRoutes(app: FastifyInstance) {
    app.post("/vehicles", {
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
    }, createVehicleController);
}
