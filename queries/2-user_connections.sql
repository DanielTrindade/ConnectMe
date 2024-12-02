SELECT 
    u.usuario_id,
    u.nome,
    u.email
FROM 
    CONEXAO c
JOIN 
    USUARIO u ON (u.usuario_id = c.usuario_id1 AND c.usuario_id2 = ?) -- subtituir o ? por pelo usuario_id de que quer procurar
               OR (u.usuario_id = c.usuario_id2 AND c.usuario_id1 = ?); -- subtituir o ? pelo mesmo usuario_id usado acima