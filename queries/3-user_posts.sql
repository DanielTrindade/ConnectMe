SELECT 
    *
FROM 
    POSTAGEM
WHERE 
    usuario_id = ?  --subtituir o ? por pelo usuario_id de que quer procurar
ORDER BY 
    data_criacao DESC;