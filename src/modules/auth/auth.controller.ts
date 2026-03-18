import { FastifyReply, FastifyRequest } from "fastify";
import { AuthService,  CreateTenantDTO} from "./auth.service.js";

const authService = new AuthService();

export async function AuthController(req: FastifyRequest, res: FastifyReply) {
    try {
        const data = req.body as CreateTenantDTO;

        const newTenant = await authService.registerTenant(data);
        
        return res.status(201).send({
            tenant: newTenant,
            message: "Tenant created successfully"
        });
    } catch (error) {
        console.log("error: ", error);
        return res.status(400).send({
            message: error instanceof Error ? error.message : "An error occurred while creating the tenant"
        });
    }
}