SELECT 
    p.postagem_id,
    p.conteudo AS conteudo_postagem,
    p.data_criacao AS data_postagem,
    p.tipo_midia,
    p.midia,
    u.nome AS nome_usuario,
    COUNT(i.interacao_id) AS total_interacoes,
    CASE 
        WHEN p.grupo_id IS NOT NULL THEN g.nome
        ELSE 'Não é de grupo'
    END AS nome_grupo
FROM 
    INTERACAO i
JOIN 
    POSTAGEM p ON i.postagem_id = p.postagem_id
JOIN 
    USUARIO u ON p.usuario_id = u.usuario_id
LEFT JOIN 
    GRUPO g ON p.grupo_id = g.grupo_id
WHERE 
    i.data >= CURDATE() - INTERVAL 7 DAY
GROUP BY 
    p.postagem_id
ORDER BY 
    total_interacoes DESC
LIMIT 5;