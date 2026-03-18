import prisma from "../../config/prisma.js";
import bcrypt from "bcrypt";
export interface CreateTenantDTO {
    tenantData: {
        businessName: string;
        document: string;
    },
    adminData: {
        name: string;
        email: string;
        password: string;
        role: string;
        createdAt: Date;
    }

}

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
        console.log(newTenant);
        
        return newTenant;
    }
}