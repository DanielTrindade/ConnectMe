SELECT 
    usuario_id,
    nome,
    email,
    municipio_id
FROM 
    USUARIO
WHERE 
    nome LIKE CONCAT('%', ?, '%'); -- substituir o ? pela string que quer procurar, ex: 'Daniel'