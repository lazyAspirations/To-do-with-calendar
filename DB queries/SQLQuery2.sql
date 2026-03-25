USE BookShelf;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tasks')
BEGIN
    CREATE TABLE Tasks (
        id INT PRIMARY KEY IDENTITY(1,1),
        date_str VARCHAR(10), -- Format YYYY-MM-DD
        task_text NVARCHAR(255),
        is_done BIT DEFAULT 0
    );
END
GO