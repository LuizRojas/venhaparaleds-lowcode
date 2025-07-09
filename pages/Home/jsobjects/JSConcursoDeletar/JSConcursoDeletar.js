export default {
  async buscarConcursoParaDeletar(codigo) {
    if (codigo.length !== 11) {
      showAlert("Digite os 11 dígitos do código do concurso.", "info");
      // BotaoDeletarConcurso.setDisabled(true);  // o botao já inicia desativado
      return;
    }

    try {
      storeValue("valorBuscaDeletarConcurso", codigo);
      storeValue("buscaConcursobyCodigo", codigo);

      const resposta = await fetchConcursosByCodigoConcurso.run();
      const statusCode = fetchConcursosByCodigoConcurso.responseMeta?.statusCode;

      if (statusCode === 404 || !resposta || Object.keys(resposta).length === 0) {
        showAlert("Concurso não encontrado!", "warning");
        TabelaInformacoesConcursoDelet.setData([]);
        BotaoDeletarConcurso.setDisabled(true);
        return;
      }

      // achoou: preenche a tabela e ativa o botão de deletar
      TabelaInformacoesConcursoDelet.setData([resposta]);
      BotaoDeletarConcurso.setDisabled(false);

    } catch (e) {
      showAlert("Erro ao buscar concurso.", "error");
      BotaoDeletarConcurso.setDisabled(true);
      TabelaInformacoesConcursoDelet.setData([]);
    }
  }
}
