import fastify from "fastify";
import { vehiclesRoutes } from "./modules/vehicles/vehicles.route";

export const app = fastify({
    logger: true,

})

app.register(vehiclesRoutes, { prefix: "/vehicle" });

app.get("/ping", async () =>{
    return { 
        message: "pong",
    }
})