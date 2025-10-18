-- Banco: estacionar-db
-- Tabela: cars_parked

USE `estacionar-db`;

INSERT INTO cars_parked (id, license_plate, model, parked, created_at, locale)
VALUES
('9cae46cb-6e16-46d7-812d-aa224826ff8e', 'MAT2K25', 'Volkswagen Nivus', 1, '2025-10-14 14:55:58', 'Subsolo 4'),
('d04db74d-fd9e-44d0-91fc-4f5fc51e7565', 'GAC5J97', 'Honda City', 1, '2025-10-14 14:49:51', 'Setor 3'),
('1a9e3f12-6c3a-4b92-9e11-81a5bfb8d221', 'FDS8G45', 'Chevrolet Onix', 1, '2025-10-14 15:05:12', 'Frente'),
('2b84a9a1-5e44-438f-b0f4-1f4b3b7c9810', 'JKL9D22', 'Fiat Argo', 1, '2025-10-14 15:12:47', 'Térreo 15'),
('3c72b6d8-1124-4f9b-8f2c-4d9acb75f998', 'QWE6T55', 'Toyota Corolla', 1, '2025-10-14 15:22:09', 'Sub 1 Vaga 15'),
('4df14d7c-0c51-4879-9418-5b76b3a9e412', 'HGR5M88', 'Jeep Compass', 0, '2025-10-14 13:43:00', 'Subsolo 2'),
('5e6fa8e9-8b71-4b3f-a1a3-c2b5f13cd557', 'PLM7U09', 'Hyundai HB20', 1, '2025-10-14 16:10:31', 'Vaga 30');
