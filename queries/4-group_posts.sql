SELECT 
    p.postagem_id,
    p.conteudo,
    p.data_criacao,
    p.tipo_midia,
    p.midia,
    p.usuario_id,
    u.nome AS nome_usuario
FROM 
    POSTAGEM p
JOIN 
    USUARIO u ON p.usuario_id = u.usuario_id
WHERE 
    p.grupo_id = ? -- substituir o ? pelo id da postagem que quer procurar
ORDER BY 
    p.data_criacao DESC
LIMIT 20;