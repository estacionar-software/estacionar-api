import { FastifyReply, FastifyRequest } from "fastify";
import { VehicleService, CreateVehicleDTO } from "./vehicles.service.js";

const vehiclesService = new VehicleService();

export async function createVehicleController(req: FastifyRequest, res: FastifyReply) {
    try {
        const data = req.body as CreateVehicleDTO;

        const newVehicle = await vehiclesService.createVehicle(data);
        
        return res.status(201).send({
            vehicle: newVehicle,
            message: "Vehicle created successfully"
        });
    } catch (error) {
        return res.status(400).send({
            message: "Error creating vehicle"
        });
    }
}