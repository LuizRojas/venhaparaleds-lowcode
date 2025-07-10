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

      // const resposta = await deleteConcursoByCodigo_Neon.run();
      // const statusCode = deleteConcursoByCodigo_Neon.responseMeta?.statusCode;
			await getConcursoCodigo_Neon.run()
			
      if (!getConcursoCodigo_Neon.data) {
        showAlert("Concurso não encontrado!", "warning");
        TabelaInformacoesConcursoDelet.setData([]);
        BotaoDeletarConcurso.setDisabled(true);
        return;
      }

      // achoou: preenche a tabela e ativa o botão de deletar
      TabelaInformacoesConcursoDelet.setData(getConcursoCodigo_Neon.data);
      BotaoDeletarConcurso.setDisabled(false);

    } catch (e) {
      showAlert("Erro ao buscar concurso.", "error");
      BotaoDeletarConcurso.setDisabled(true);
      TabelaInformacoesConcursoDelet.setData([]);
    }
  }
}
