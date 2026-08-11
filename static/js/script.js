// KNOWLIBRAS — funções utilitárias compartilhadas entre as páginas
// Usado por: index.html, categoria.html, termo.html

/**
 * Lê um parâmetro da query string da URL atual.
 * Ex: getParam("cat") em "termo.html?cat=bd&termo=sql" retorna "bd"
 */
function getParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

/**
 * Remove acentos e deixa em minúsculo, pra busca não ser sensível
 * a maiúsculas/acentuação (ex: "banco de dados" == "Banco de Dados")
 */
function normalizar(texto) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

/**
 * Busca termos pelo título em todas as categorias de KNOWLIBRAS_DATA.
 * Retorna uma lista de objetos { catId, termId, title }
 */
function buscarTermos(query) {
  const termoBusca = normalizar(query.trim());
  const resultados = [];

  if (!termoBusca) return resultados;

  Object.entries(KNOWLIBRAS_DATA).forEach(([catId, categoria]) => {
    Object.entries(categoria.terms).forEach(([termId, termo]) => {
      if (normalizar(termo.title).includes(termoBusca)) {
        resultados.push({ catId, termId, title: termo.title });
      }
    });
  });

  return resultados;
}