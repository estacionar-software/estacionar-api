import prisma from "../../config/prisma.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { env } from "../../config/env.js";
import { CreateTenantDTO } from "./auth.schema.js";


export class AuthService {
    async registerTenant(data: CreateTenantDTO){

        const emailExists = await prisma.user.findUnique({
            where: {
                email: data.adminData.email,
            }
        })

        if(emailExists){
            throw new Error("Email already exists");
        }

        const documentExists = await prisma.tenant.findUnique({
            where: {
                document: data.tenantData.document,
            }
        })

        if(documentExists){
            throw new Error("Tenant document already exists");
        }

        const passwordHash = await bcrypt.hash(data.adminData.password, 10);

        const newTenant = await prisma.tenant.create({
            data: {
                businessName: data.tenantData.businessName,
                document: data.tenantData.document,
                    users: {
                        create: {
                        name: data.adminData.name,
                        email: data.adminData.email,
                        passwordHash: passwordHash,
                        role: "ADMIN",
                        createdAt: data.adminData.createdAt,
                    }
                }
            }
        })
        
        return newTenant;
    }

    async Login(email: string, password: string) {


        const user = await prisma.user.findUnique({
            where: {
                email: email,
            }
        })
        
        if(!user){
            throw new Error("Invalid email or password");
        }

        const passwordMatch = await bcrypt.compare(password, user.passwordHash);
        
        if(!passwordMatch){
            throw new Error("Invalid email or password");
        }

        const { passwordHash, ...userWithoutPassword } = user;

        if(!env.jwtSecret) {
            throw new Error("JWT secret is not defined in environment variables");
        }

        const token = jwt.sign(userWithoutPassword, env.jwtSecret, {
            expiresIn: "6h",
        })

        return {
            ...userWithoutPassword,
            token
        };
    }

}