import { FastifyReply, FastifyRequest } from "fastify";
import { AuthService} from "./auth.service.js";
import { CreateTenantDTO, LoginDTO } from "./auth.schema.js";

const authService = new AuthService();

export async function CreateTenantController(req: FastifyRequest, res: FastifyReply) {
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

export async function LoginController(req: FastifyRequest, res: FastifyReply) {
    try {
        const data = req.body as LoginDTO;

        const user = await authService.Login(data.email, data.password);

        
        return res.status(200).send({
            user,
            message: "Login successful"
        });
    } catch (error) {   
        console.log("error: ", error);
        return res.status(400).send({
            message: error instanceof Error ? error.message : "An error occurred while logging in"
        });
        }
}