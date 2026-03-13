import { db } from "../../database";

export interface CreateVehicleDTO {
    licensePlate: string;
    model: string;
    locale: string;
}

export class VehicleService {
    async createVehicle(data: CreateVehicleDTO) {

        const result = await db.query(
            `INSERT INTO vehicles (license_plate, model, locale) VALUES ($1, $2, $3) RETURNING *`,
            [data.licensePlate.toUpperCase(), data.model, data.locale]
        );

        const plateFormated = data.licensePlate.toUpperCase();

        const newVehicle = {
            id: crypto.randomUUID(),
            createdAt: new Date().toISOString(),
            licensePlate: plateFormated,
            model: data.model,
            locale: data.locale,
        }

        return newVehicle;
        }
}