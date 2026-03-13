import prisma from "../../lib/prisma";
export interface CreateUserDTO {
    name: string;
    email: string;
    password: string;
}

export class AuthService {
    async registerTenant(data: CreateUserDTO){

    }
}