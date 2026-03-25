import fastify, { FastifyReply, FastifyRequest } from "fastify";
import { AuthRoutes } from "./modules/auth/auth.route.js";
import { verifyToken } from "./middlewares/auth.middleware.js";

export const app = fastify({
    logger: true,

})

app.register(AuthRoutes, { prefix: "/auth" });

app.get("/ping", { preHandler: verifyToken }, async (req: FastifyRequest, res: FastifyReply) =>  {
    const { email, name, role } = req.user;

    return res.send({ id: email, name, role, message: "pong", });
})