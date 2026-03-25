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

export interface LoginDTO {
    email: string;
    password: string;
}

export interface UserDTO {
    id: string;
    name: string;
    email: string;
    role: string;
    createdAt: Date;
}