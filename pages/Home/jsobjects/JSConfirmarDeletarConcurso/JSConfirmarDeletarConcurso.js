export default {
  limparCampos() {
    EntradaDeletarConcursoBusca.setValue("");
    TabelaInformacoesConcursoDelet.setData([]);
    BotaoDeletarConcurso.setDisabled(true);
    // removeValue("valorBuscaDeletarConcurso");
		// removeValue("buscaConcursobyCodigo");
  },

  async confirmarDeletarConcurso() {
    try {
      await deleteConcursoAPI.run();
      showAlert(
        "Concurso com código " + appsmith.store.buscaConcursobyCodigo + " foi deletado com sucesso!",
        "info"
      );
      showModal(ModalDeletarConcursos.name);
    } catch (e) {
      showAlert("Erro ao deletar o concurso!", "error");
      console.log("Erro ao deletar:", e);
    }
  }
}