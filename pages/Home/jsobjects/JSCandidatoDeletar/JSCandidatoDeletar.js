export default {
  async buscarCandidatoParaDeletar(cpf) {
    const cpf_limpo = cpf.replace(/\D/g, "").trim();  // remove tudo que não for número
    console.log("CPF limpo:", cpf_limpo);
    console.log("Tamanho:", cpf_limpo.length);

    if (cpf_limpo.length !== 11) {
      showAlert("Padrão de CPF incorreto, verifique a quantidade de dígitos.", "info");
      return;
    }

    try {
      storeValue("valorBuscaDeletarCandidato", cpf_limpo);
      storeValue("buscaCandidatoByCPF", cpf_limpo);

      const resposta = await fetchCandidatosByCPF.run();
      const statusCode = fetchCandidatosByCPF.responseMeta?.statusCode;

      if (statusCode === 404 || !resposta || Object.keys(resposta).length === 0) {
        showAlert("Candidato não encontrado!", "warning");
        TabelaInformacoesCandidatosDel.setData([]);
        BotaoDeletarCandidato.setDisabled(true);
        return;
      }

      // Achou: preenche a tabela e ativa o botão de deletar
      TabelaInformacoesCandidatosDel.setData([resposta]);
      BotaoDeletarCandidato.setDisabled(false);

    } catch (e) {
      console.log("Erro:", e);
      showAlert("Erro ao buscar candidato.", "error");
      BotaoDeletarCandidato.setDisabled(true);
      TabelaInformacoesCandidatosDel.setData([]);
    }
  }
}
