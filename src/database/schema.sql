CREATE EXTENSION IF NOT EXISTS "pgcrypto"; ---EXTENSÃO PARA GERAR UUIDS

-- ======================================================================
-- FUNÇÃO ÚTIL PARA ATUALIZAR O CAMPO updated_at AUTOMATICAMENTE
-- ======================================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ======================================================================
-- TENANTS (Clientes / Estacionamentos)
-- ======================================================================
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name VARCHAR(100) NOT NULL,
    document VARCHAR(20), 
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER tg_tenants_updated_at
BEFORE UPDATE ON tenants
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ======================================================================
-- SESSÕES DE ESTACIONAMENTO (cars_parked e cars_parked_history numa só tabela)
-- ======================================================================
CREATE TABLE parking_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    license_plate VARCHAR(10) NOT NULL,
    model VARCHAR(80) NOT NULL,
    locale VARCHAR(80) NOT NULL,
    is_parked BOOLEAN NOT NULL DEFAULT TRUE,
    entry_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMPTZ, -- Fica NULO enquanto o carro não sair (checkout)
    total_time_minutes INTEGER,
    total_price NUMERIC(10,2), 
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER tg_parking_sessions_updated_at
BEFORE UPDATE ON parking_sessions
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX idx_sessions_tenant_plate ON parking_sessions(tenant_id, license_plate);
CREATE INDEX idx_sessions_active ON parking_sessions(tenant_id) WHERE is_parked = TRUE;

-- ======================================================================
-- CONFIGURAÇÃO DE PREÇOS (parking_fees)
-- ======================================================================
CREATE TABLE parking_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    quick_stop_price NUMERIC(10,2) NOT NULL,
    until_time_price NUMERIC(10,2) NOT NULL,
    extra_hour_price NUMERIC(10,2) NOT NULL,
    quick_stop_limit_minutes INTEGER NOT NULL,
    parking_hours INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_tenant_price UNIQUE(tenant_id) 
);

CREATE TRIGGER tg_parking_prices_updated_at
BEFORE UPDATE ON parking_prices
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ======================================================================
-- PRODUTOS E SERVIÇOS
-- ======================================================================
-- Criação de um ENUM para travar os tipos aceitos pela API
CREATE TYPE product_type_enum AS ENUM ('product', 'service');

CREATE TABLE products_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    amount INTEGER DEFAULT 0, 
    price NUMERIC(10,2) NOT NULL,
    type product_type_enum NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER tg_products_services_updated_at
BEFORE UPDATE ON products_services
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX idx_products_tenant ON products_services(tenant_id);