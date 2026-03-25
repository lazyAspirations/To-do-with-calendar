USE BookShelf;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Settings')
BEGIN
    CREATE TABLE Settings (
        id INT PRIMARY KEY DEFAULT 1,
        is_dark_mode BIT DEFAULT 1,
        CONSTRAINT one_row CHECK (id = 1) -- Assure qu'on ne garde qu'une seule ligne de config
    );
    -- Insertion de la configuration par défaut
    INSERT INTO Settings (id, is_dark_mode) VALUES (1, 1);
END
GO