

export interface CreateVehicleDTO {
    licensePlate: string;
    model: string;
    locale: string;
}

export class VehicleService {
    async createVehicle(data: CreateVehicleDTO) {

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