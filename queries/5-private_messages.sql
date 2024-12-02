SELECT 
    mensagem_id,
    conteudo,
    data_envio,
    remetente_id,
    destinatario_id
FROM 
    MENSAGEM
WHERE 
    (remetente_id = ? AND destinatario_id = ?) -- ex: subtituir o 1° ? por 2 e o 2° por 3
    OR (remetente_id = ? AND destinatario_id = ?) -- ex: subtituir o 1° ? por 3 e o 2° por 2
ORDER BY 
    data_envio DESC
LIMIT 10;