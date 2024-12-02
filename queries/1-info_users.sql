SELECT 
  u.usuario_id, 
  u.nome, 
  u.email, 
  u.foto, 
  u.biografia, 
  u.data_nascimento,
  m.nome AS municipio,
  e.nome AS estado,
  e.uf
FROM USUARIO u
JOIN MUNICIPIO m ON u.municipio_id = m.municipio_id
JOIN ESTADO e ON m.estado_id = e.estado_id
WHERE usuario_id = ?;--substituir o ? pelo usuario_id que quer procurar