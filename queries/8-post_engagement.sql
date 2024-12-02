SELECT 
    COUNT(DISTINCT i.usuario_id) AS total_usuarios_interagiram
FROM 
    INTERACAO i
JOIN 
    POSTAGEM p ON i.postagem_id = p.postagem_id
WHERE 
    p.postagem_id = ?  -- Substitua '?' pelo postagem_id do post desejado
    AND i.data >= CURDATE() - INTERVAL 7 DAY;