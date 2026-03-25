import { FastifyRequest, FastifyReply } from "fastify";
import jwt from "jsonwebtoken";
import { env } from "../config/env.js";
import { UserDTO } from "../modules/auth/auth.schema.js";

export async function verifyToken(req: FastifyRequest, res: FastifyReply) {
    try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return res.status(401).send({ message: "Token não fornecido" });
    }

    const token = authHeader.split(" ")[1];
    
        const decoded = jwt.verify(token, env.jwtSecret as string) as UserDTO;
        req.user = decoded;
    } catch (error) {
        return res.status(401).send({ message: "Token inválido ou expirado" });
    }
}