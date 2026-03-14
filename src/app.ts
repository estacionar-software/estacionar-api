import fastify from "fastify";
import { vehiclesRoutes } from "./modules/vehicles/vehicles.route";
import { AuthRoutes } from "./modules/auth/auth.route";

export const app = fastify({
    logger: true,

})

app.register(vehiclesRoutes, { prefix: "/vehicle" });
app.register(AuthRoutes, { prefix: "/auth" });

app.get("/ping", async () =>{
    return { 
        message: "pong",
    }
})